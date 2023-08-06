/*
  This software is Copyright (C) 2021-2022 by Ben Cahill and 2006-2022 by James C. Ahlstrom,
  and is licensed for use under the GNU General Public License (GPL).
  See http://www.opensource.org.
  Note that there is NO WARRANTY AT ALL.  USE AT YOUR OWN RISK!!
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <complex.h>
#include <math.h>
#include <sys/time.h>
#include <time.h>
#include <errno.h>

#ifdef MS_WINDOWS
#include <winsock2.h>
#include <stdint.h>
#else
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#endif

#include "../quisk.h"

#define REMOTE_DEBUG 0  //BMC TODO:  Make this a configuration option

// For remote control sound; 2 sockets used at each end, but 4 needed to guide program flow
static SOCKET radio_sound_to_control_head_socket = INVALID_SOCKET;	// send radio sound to control_head
static SOCKET radio_sound_from_remote_radio_socket = INVALID_SOCKET;	// receive radio sound from remote_radio
static SOCKET mic_sound_from_control_head_socket = INVALID_SOCKET;	// receive mic sound from control_head
static SOCKET mic_sound_to_remote_radio_socket = INVALID_SOCKET;	// send mic sound to remote_radio
static int sound_from_remote_socket_started = 0;			// sound (radio or mic) stream started from far end
static int sound_to_remote_socket_started = 0;				// sound (radio or mic) stream started from near end
static int packets_sent;
static int packets_recd;

static void send_remote_sound_socket(SOCKET * sock, complex double * cSamples, int nSamples);

// Receive stereo 16-bit pcm sound via UDP
// This code acts as UDP client for radio sound (on control head)
int read_remote_radio_sound_socket(struct sound_dev* dev, complex double * cSamples, int nSamples)
{
	int i;
	int bytes = 0;
	double samp_r, samp_l;
	int16_t * ptInt16;
	int lapcount = 0;
	struct timeval tm_wait;
	fd_set fds;
	SOCKET * sock = &radio_sound_from_remote_radio_socket;
	// static okay if only one instance runs, which should be good assumption when running remote
	static char buf[128000];	// TODO:  Calculate based on remote sound latency setting
	static int prebuf_samples = 48000 / 10; // 100 msec (TODO:  replace with calculation)
	static int prebuf_done = 0;
	static int rd_idx = 0;	// bytes
	static int wr_idx = 0;	// bytes
	static int wrap_idx;	// bytes
	static int samps_in_buf = 0;	// samples (4 bytes per sample)
	static int underrun_count = 0;	// samples
	static size_t prior_pkt_size_max = 0;

#if REMOTE_DEBUG > 0 //BMC debug -- summary every 200 calls
	// measure/monitor tools:
	static float callcount = 0;
	static float sampcount_in = 0;
	static float sampcount_out = 0;
	static float nSamps = 0;
	static uint64_t bunchcount = 0;
	static float callcount_total = 0;
	static float sampcount_in_total = 0;
	static float sampcount_out_total = 0;
	static float nSamps_total = 0;
	static double delta_total = 0;
	static double prior_ts = 0;
#endif

	if (*sock == INVALID_SOCKET)
		return 0;

#if REMOTE_DEBUG > 0 //BMC debug -- summary every 200 calls
	nSamps += nSamples;
	callcount++;
#endif
	// Signal far end (server) that we're ready (this sends our address/port to far end)
	if (!sound_from_remote_socket_started) {
		printf("read_remote_radio_sound_socket() sending 'rr', *sock = %u\n", (u_int)*sock);
		bytes = send(*sock, "rr\n", 3, 0);
		if (bytes != 3)
			printf("read_remote_radio_sound_socket(), sendto(): %s\n", strerror(errno));
	}

	// read all available packets, one per loop, place into jitter-absorbing circular buffer
	while (1) {
		int buftop;
		char * wr_base;
		size_t wr_len;
		lapcount++;
		// set up for direct receive into circular buffer
		wr_base = &buf[wr_idx];
		if (wr_idx > rd_idx || samps_in_buf == 0)
			buftop = sizeof(buf);
		else
			buftop = rd_idx;
		wr_len = buftop - wr_idx;	// contiguous (non-wrapping) space available in buffer
		if (wr_len < prior_pkt_size_max && prior_pkt_size_max > 0) {
			if (wr_idx > rd_idx || samps_in_buf == 0) {
				// wrap before recv() so data expected in recv() fits within contiguous (non-wrapping) space
				wrap_idx = wr_idx;
				wr_idx = 0;
				wr_base = &buf[0];
				if (samps_in_buf == 0)
					wr_len = sizeof(buf);
				else
					wr_len = rd_idx;
#if REMOTE_DEBUG > 2 //BMC debug
				printf("wrapping write at wrap_idx = %i, rd_idx = %i, wr_len = %li\n", wrap_idx, rd_idx, wr_len);
#endif
			}
#if REMOTE_DEBUG > 0
			else {
				double now = QuiskTimeSec();
				printf("%f, jitbuf overflow, reduce recv fm %u to %u, wr_idx %u, rd_idx %u, samps_in_buf %u, remainder 0s\n",
					now, (u_int)prior_pkt_size_max, (u_int)wr_len, wr_idx, rd_idx, samps_in_buf);
			}
#endif
		}

		tm_wait.tv_sec = 0;
		tm_wait.tv_usec = 0;
		FD_ZERO (&fds);
		FD_SET (*sock, &fds);
		if (select(*sock + 1, &fds, NULL, NULL, &tm_wait) != 1) {
			//BMC printf("read_remote_radio_sound_socket(): select returned %i\n", retval);
			bytes = 0;
			break;
		}
		bytes = recv(*sock, wr_base, wr_len, 0);
		if (bytes < 0) {
			int err = errno;
			if (err != EAGAIN && err != EWOULDBLOCK)
				printf("read_remote_radio_sound_socket(), recv(): %s\n", strerror(errno));
			break;
		}
		if (bytes > 0) {
			sound_from_remote_socket_started = 1;
			packets_recd++;
			wr_idx += bytes;
			if ((size_t)bytes > prior_pkt_size_max)
				prior_pkt_size_max = bytes;
			samps_in_buf += bytes / 4;	//TODO:  Calculate using sizeof
#if REMOTE_DEBUG > 0 //BMC debug -- for summary every 200 calls
			sampcount_in += bytes / 4;
#endif
		}
	} // while(1)
	if (!sound_from_remote_socket_started  && bytes > 0) {
		printf("read_remote_radio_sound_socket(): Started! samps_in_buf = %i\n", bytes / 4);
		sound_from_remote_socket_started = 1;
	}
	if (!prebuf_done) {
		if (samps_in_buf >= prebuf_samples) {
			prebuf_done = 1;
			printf("read_remote_radio_sound_socket: Prebuf done, samps_in_buf = %i\n", samps_in_buf);
		}
	}

	if (quisk_play_state > RECEIVE && dev->dev_index == t_Playback) {
		// TX time for Radio Sound client ...
		if (samps_in_buf > prebuf_samples * 2 && underrun_count > prebuf_samples / 4) {
			// Network delays may cause radio sound jitter buffer underruns, but the incoming sound samples eventually
			// arrive from the network, causing the jitter buffer to contain *more* samples than desired,
			// perhaps even causing jitbuf overflows (so don't use underrun_count to calculate # samples to remove).
			// Use Tx time to remove excess samples to keep playback latency short;
			//     set rd_idx so there is prebuf_samples number of samples in buffer.
#if REMOTE_DEBUG > 0
			double now = QuiskTimeSec();
			printf("%f, Removing excess jitbuf samples: underrun_count %i, samps_in_buf %i, rd_idx %i, wrap_idx %i, wr_idx %i\n",
					now, underrun_count, samps_in_buf, rd_idx, wrap_idx, wr_idx);
#endif
			rd_idx = wr_idx - (prebuf_samples * 4);	// rd_idx = bytes; prebuf_samples = samples; 4 bytes per sample
			if (rd_idx < 0)
				rd_idx += wrap_idx;
			samps_in_buf = prebuf_samples;
			underrun_count = 0;
#if REMOTE_DEBUG > 0
			printf("%f, Removed excess jitbuf samples: samps_in_buf %i, rd_idx %i, wrap_idx %i,\n",
					now, samps_in_buf, rd_idx, wrap_idx);
#endif
		}
		if (quisk_active_sidetone == 4) {
			// Overwrite remote sound with sidetone, starting at jitter buffer read position
			int tmp_idx = rd_idx;
			ptInt16 = (int16_t *)&buf[tmp_idx];
			for (i = 0; i < nSamples; i++) {
				int16_t * ptSamples = quisk_make_sidetone(dev, 0);
				*ptInt16++ = *ptSamples;
				*ptInt16++ = *ptSamples;
				tmp_idx += 4;
				if (tmp_idx >= wrap_idx && wrap_idx != 0) {
					tmp_idx = 0;
					ptInt16 = (int16_t *)&buf[tmp_idx];
#if 0 //BMC debug
					printf("wrapping sidetone at wrap_idx = %i\n", wrap_idx);
#endif
				}
			}
		}
	}


	if (prebuf_done) {
		int numout = nSamples;
		int newSamples = 0;
		if (samps_in_buf < nSamples) {
			double now = QuiskTimeSec();
			numout = samps_in_buf;
			underrun_count += (nSamples - samps_in_buf);
			printf("%f, jitbuf low, reduce outsamps fm %i to %i, wr_idx %i, rd_idx %i, samps_in_buf %i, remainder 0s\n",
				now, nSamples, numout, wr_idx, rd_idx, samps_in_buf);
		}
		ptInt16 = (int16_t *)&buf[rd_idx];
		for (i = 0; i < numout; i++) {
			samp_r = *ptInt16++;
			samp_l = *ptInt16++;
			cSamples[newSamples++] = (samp_r + I * samp_l) / CLIP16 * CLIP32;
#if REMOTE_DEBUG > 0 //BMC debug -- for summary every 200 calls
			sampcount_out++;
#endif
			samps_in_buf--;
			rd_idx += 4;
			if (rd_idx >= wrap_idx && wrap_idx != 0) {
				rd_idx = 0;
				ptInt16 = (int16_t *)&buf[rd_idx];
#if REMOTE_DEBUG > 2 //BMC debug
				printf("wrapping read at wrap_idx = %i\n", wrap_idx);
#endif
			}
		}
	}

#if REMOTE_DEBUG > 1 //BMC debug -- per-call (perhaps multi-packet) statistics
	if (lapcount != 1) {	// 1: 0 packets, 2: 1 packet, 3: 2 packets, etc.
		double ts = QuiskTimeSec();
		printf("%f: callcount = %lu, lapcount = %i, bytes = %i, nSamples = %i\n", ts, callcount, lapcount, bytes, nSamples);
	}
#endif

#if REMOTE_DEBUG > 0 //BMC debug -- summary every 200 calls (a little over one second)
	if (callcount >= 200) {
		double new_ts = QuiskTimeSec();
		double delta = new_ts - prior_ts;
		prior_ts = new_ts;
#if REMOTE_DEBUG > 2 //BMC raw numbers
		printf("%f: read_remote_radio_sound_socket CURRENT calls: %lu, samps_in %lu, samps_out %lu, nSamps %lu, samps_in_buf %i, deltasec %f\n",
			new_ts, callcount, sampcount_in, sampcount_out, nSamps, samps_in_buf, delta);
#endif
#if REMOTE_DEBUG > 1 //BMC raw numbers
		printf("%f: read_remote_radio_sound_socket CURRENT RATES (HZ): calls %f, samps_in %f, samps_out %f, nSamps %f, samps_in_buf %i\n",
			new_ts, callcount / delta, sampcount_in / delta, sampcount_out / delta, nSamps / delta, samps_in_buf);
#endif
		if (bunchcount > 0) {	// skip the initial bunch; prebuf may distort some numbers(?)
			callcount_total += callcount;
			sampcount_in_total += sampcount_in;
			sampcount_out_total += sampcount_out;
			nSamps_total += nSamps;
			delta_total += delta;
		}
		if (bunchcount % 10 == 0 && bunchcount > 0) {
#if REMOTE_DEBUG > 1 //BMC
			printf("%f: read_remote_radio_sound_socket SUMMARY calls: %f, samps_in %f, samps_out %f, nSamps %f, samps_in_buf %i, deltasec %f\n",
				new_ts, callcount_total, sampcount_in_total, sampcount_out_total, nSamps_total, samps_in_buf, delta_total);
			printf("%f: read_remote_radio_sound_socket SUMMARY RATES (HZ): calls %f, samps_in %f, samps_out %f, nSamps %f\n",
				new_ts, callcount_total / delta_total, sampcount_in_total / delta_total,
				sampcount_out_total / delta_total, nSamps_total / delta_total);
#else
			float latency = (float)samps_in_buf / 48000.0;
			printf("%f: read_remote_radio_sound_socket samps_in_buf %i, latency %f sec\n", new_ts, samps_in_buf, latency);
#endif
		}
		bunchcount++;
		callcount = 0;
		sampcount_in = 0;
		sampcount_out = 0;
		nSamps = 0;
	}
#endif
	// Always return same # samples sent in, even if we didn't change any
	return nSamples;
}



// Receive stereo 16-bit pcm sound via UDP
// This code acts as UDP client for mic sound (on remote radio)
int read_remote_mic_sound_socket(struct sound_dev* dev, complex double * cSamples)
{
	int i;
	int bytes = 0;
	double samp_r, samp_l;
	int16_t * ptInt16;
	int rd_idx = 0;	// bytes
	int wr_idx = 0;	// bytes
	int samps_in_buf = 0;	// samples (4 bytes per sample)
	int lapcount = 0;
	struct timeval tm_wait;
	fd_set fds;
	SOCKET * sock = &mic_sound_from_control_head_socket;
	// static okay if only one instance runs, which should be good assumption when running remote
	static char buf[128000];	// TODO:  Calculate based on ???

	if (*sock == INVALID_SOCKET)
		return 0;

	// Signal far end (server) that we're ready (this sends our address/port to far end)
	if (!sound_from_remote_socket_started) {
		printf("read_remote_mic_sound_socket() sending 'rr', *sock = %u\n", (u_int)*sock);
		bytes = send(*sock, "rr\n", 3, 0);
		if (bytes != 3)
			printf("read_remote_mic_sound_socket(), sendto(): %s\n", strerror(errno));
	}

	// read all available packets, one per loop, place into jitter-absorbing circular buffer
	while (1) {
		int buftop = sizeof(buf);
		char * wr_base;
		size_t wr_len;
		lapcount++;
		// set up for direct receive into linear buffer
		wr_base = &buf[wr_idx];
		wr_len = buftop - wr_idx;	// remaining contiguous space available in buffer

		tm_wait.tv_sec = 0;
		tm_wait.tv_usec = 0;
		FD_ZERO (&fds);
		FD_SET (*sock, &fds);
		if (select(*sock + 1, &fds, NULL, NULL, &tm_wait) != 1) {
			//BMC printf("read_remote_mic_sound_socket(): select returned %i\n", retval);
			bytes = 0;
			break;
		}
		bytes = recv(*sock, wr_base, wr_len, 0);
		if (bytes < 0) {
			int err = errno;
			if (err != EAGAIN && err != EWOULDBLOCK)
				printf("read_remote_mic_sound_socket(), recv(): %s\n", strerror(errno));
			break;
		}
		if (bytes > 0) {
			sound_from_remote_socket_started = 1;
			packets_recd++;
			wr_idx += bytes;
			samps_in_buf += bytes / 4;	//TODO:  Calculate using sizeof
		}
	} // while(1)

	if (!sound_from_remote_socket_started  && bytes > 0) {
		printf("read_remote_mic_sound_socket(): Started! samps_in_buf = %i\n", bytes / 4);
		sound_from_remote_socket_started = 1;
	}

	ptInt16 = (int16_t *)&buf[rd_idx];
	for (i = 0; i < samps_in_buf; i++) {
		samp_r = *ptInt16++;
		samp_l = *ptInt16++;
		cSamples[i] = (samp_r + I * samp_l) / CLIP16 * CLIP32;
		rd_idx += 4;
	}

	return samps_in_buf;
}
// Send stereo 16-bit pcm sound via UDP
// This code acts as UDP server for radio sound (on remote radio) or mic sound (on control head)
#define MAX_SAMPLES_FOR_REMOTE_SOUND 15000
#define RX_BUFFER_SIZE 64

void send_remote_radio_sound_socket(complex double * cSamples, int nSamples)
{
	send_remote_sound_socket(&radio_sound_to_control_head_socket, cSamples, nSamples);
}

void send_remote_mic_sound_socket(complex double * cSamples, int nSamples)
{
	send_remote_sound_socket(&mic_sound_to_remote_radio_socket, cSamples, nSamples);
}

static void send_remote_sound_socket(SOCKET * sock, complex double * cSamples, int nSamples)
{	// Send nSamples samples.  Each sample is sent as two shorts (4 bytes) of L/R audio data.
	int i, sent;
	short sound_lr[MAX_SAMPLES_FOR_REMOTE_SOUND * 2]; // Limit Tx to 60,000 bytes, 30,000 shorts, 15,000 samples
	int udp_size = 0;	// Keep track of UDP payload size, in shorts
	char buf[RX_BUFFER_SIZE];	// For startup message
	int recv_len;
	int retval;

#if REMOTE_DEBUG > 0 //BMC debug
	// measure/monitor tools:
	static float callcount = 0;
	static float sampcount = 0;
	static uint64_t bunchcount = 0;
	static float callcount_total = 0;
	static float sampcount_total = 0;
	static double prior_ts = 0;
	static double delta_total = 0;
#if REMOTE_DEBUG > 1 //BMC debug
	static double prior_packet_ts = 0.0;
	double now;
#endif
#endif

	if (*sock == INVALID_SOCKET)
		return;

#if REMOTE_DEBUG > 0 //BMC debug
	callcount++;
#endif
	// Wait for far end (client) to send its opening greetings, so we can grab its network address/port
	if (!sound_to_remote_socket_started) {
		struct sockaddr_in far_addr;
#ifdef MS_WINDOWS
		int addr_len = sizeof(struct sockaddr_in);
#else
		socklen_t addr_len = sizeof(struct sockaddr_in);
#endif
		struct timeval tm_wait;
		fd_set fds;
		tm_wait.tv_sec = 0;
		tm_wait.tv_usec = 0;
		FD_ZERO (&fds);
		FD_SET (*sock, &fds);
		if ((retval = select(*sock + 1, &fds, NULL, NULL, &tm_wait)) != 1) {
			//BMC printf("send_remote_sound_socket(): select returned %i\n", retval);
			return;
		}
		// Receive short msg, grab far end address
		if ((recv_len = recvfrom(*sock, buf, RX_BUFFER_SIZE, 0, (struct sockaddr *) &far_addr, &addr_len)) == -1) {
			printf("send_remote_sound_socket(), recvfrom(): %s\n", strerror(errno));
			return;
		}
		else if(recv_len > 0) {
			if (recv_len >= RX_BUFFER_SIZE)
				buf[RX_BUFFER_SIZE - 1] = '\n';
			else
				buf[recv_len] = '\n';
			printf("send_remote_sound_socket(): recv_len = %i, %s", recv_len, buf);
			if (connect(*sock, (const struct sockaddr *)&far_addr, sizeof(far_addr)) != 0) {
				printf("send_remote_sound_socket), connect(): %s\n", strerror(errno));
				close(*sock);
				*sock = INVALID_SOCKET;
			}
			else
				sound_to_remote_socket_started = 1;
		}
	}

	if (nSamples > MAX_SAMPLES_FOR_REMOTE_SOUND) {
		printf("send_remote_sound_socket():  nSamples %i > MAX_SAMPLES_FOR_REMOTE_SOUND 15,000, trimming to MAX\n", nSamples);
		nSamples = MAX_SAMPLES_FOR_REMOTE_SOUND;
	}

	// Convert format from complex double to stereo pairs of 16-bit PCM samples, send to client
	for (i = 0; i < nSamples; i++) {
		sound_lr[udp_size++] = (short)(creal(cSamples[i]) * (double)CLIP16 / CLIP32);
		sound_lr[udp_size++] = (short)(cimag(cSamples[i]) * (double)CLIP16 / CLIP32);
	}
	if (udp_size > 0) {
		sent = send(*sock, (char *)sound_lr, udp_size * 2, 0);
		if (sent != udp_size * 2)
			printf("send_remote_sound_socket(), send(): %s\n", strerror(errno));
#if REMOTE_DEBUG > 0 //BMC debug
		else {
			sampcount += sent/4;
			packets_sent++;
#if REMOTE_DEBUG > 1 //BMC debug
			now = QuiskTimeSec();
			printf("%f, send_remote_sound_socket(): now - prior = %f, samples = %u, sampcount = %lu\n",
				now, now - prior_packet_ts, sent / 4, sampcount);
			prior_packet_ts = now;
#endif
		}
#endif
	}
#if REMOTE_DEBUG > 1 //BMC debug
	else {
		now = QuiskTimeSec();
		printf("%f, send_remote_sound_socket(): nSamples = %i\n", now, nSamples);
	}
#endif
#if REMOTE_DEBUG > 0 //BMC debug
	if (callcount >= 200) {
		double new_ts = QuiskTimeSec();
		double delta = new_ts - prior_ts;
		prior_ts = new_ts;
#if REMOTE_DEBUG > 1 //BMC every 200
		printf("send_remote_sound_socket CURRENT calls: %lu, samples %lu, deltasec %f\n", callcount, sampcount, delta);
		printf("%f: send_remote_sound_socket CURRENT RATES (HZ): calls %f, samples %f\n", new_ts, callcount / delta, sampcount / delta);
#endif
		if (bunchcount > 0) {	// skip the initial bunch; prebuf may distort some numbers(?)
			callcount_total += callcount;
			sampcount_total += sampcount;
			delta_total += delta;
		}
		if (bunchcount % 10 == 0 && bunchcount > 0) {
			printf("%f: send_remote_sound_socket SUMMARY calls: %f, samples %f, deltasec %f\n",
				new_ts, callcount_total, sampcount_total, delta_total);
			printf("%f: send_remote_sound_socket SUMMARY RATES (HZ): calls %f, samples %f\n",
				new_ts, callcount_total / delta_total, sampcount_total / delta_total);
		}
		bunchcount++;
		callcount = 0;
		sampcount = 0;
	}
#endif
}



static int start_winsock()
{
#ifdef MS_WINDOWS
	WORD wVersionRequested = MAKEWORD(2, 2);
	WSADATA wsaData;

	if (WSAStartup(wVersionRequested, &wsaData) != 0) {
		printf("start_winsock(): %s\n", strerror(errno));
		return 0;		// failure to start winsock
	}
#endif
	return 1;
}





static void open_remote_sound_server(SOCKET * sock, char * ip, int port, int sndsize, char * name)
{
	struct sockaddr_in bind_addr;
	const char enable = 1;	// for sockopt
#ifndef MS_WINDOWS
	int tos = 184;	// DSCP "Expedite" (46)
#endif

	if (!start_winsock()) {
		printf("open_remote_sound_server for %s: Failure to start WinSock\n", name);
		return;
	}

	*sock = socket(PF_INET, SOCK_DGRAM, 0);
	if (*sock != INVALID_SOCKET) {
		setsockopt(*sock, SOL_SOCKET, SO_SNDBUF, (char *)&sndsize, sizeof(sndsize));
		setsockopt(*sock, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable));
#ifndef MS_WINDOWS
		setsockopt(*sock, IPPROTO_IP, IP_TOS, &tos, sizeof(tos));
#endif

		// bind to this computer for receiving (and reading far-end address from client)
		memset((char *) &bind_addr, 0, sizeof(bind_addr));
		bind_addr.sin_family = AF_INET;
		bind_addr.sin_port = htons(port);
		bind_addr.sin_addr.s_addr = htonl(INADDR_ANY);
		if (bind(*sock, (const struct sockaddr *)&bind_addr, sizeof(bind_addr)) != 0) {
			printf("open_remote_sound_server(), bind(): %s\n", strerror(errno));
			close(*sock);
			*sock = INVALID_SOCKET;
		}
	}
	if (*sock == INVALID_SOCKET) {
		printf("open server %s: Failure to open socket\n", name);
	}
	else {
		printf("open server %s: opened socket %s port %i\n", name, ip, port);
	}
}


static void open_remote_sound_client(SOCKET * sock, char * ip, int port, int sndsize, char * name)
{
	struct sockaddr_in Addr;
	const char enable = 1;	// for sockopt

	if (!start_winsock()) {
		printf("open_remote_sound_client for %s: Failure to start WinSock\n", name);
		return;
	}

	*sock = socket(PF_INET, SOCK_DGRAM, 0);
	if (*sock != INVALID_SOCKET) {
		setsockopt(*sock, SOL_SOCKET, SO_RCVBUF, (char *)&sndsize, sizeof(sndsize));
		setsockopt(*sock, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable));

		// set far-end address structure to enable sending initial packet to get things started
		Addr.sin_family = AF_INET;
		Addr.sin_port = htons(port);
#ifdef MS_WINDOWS
		Addr.sin_addr.S_un.S_addr = inet_addr(ip);
#else
		inet_aton(ip, &Addr.sin_addr);
#endif
		if (connect(*sock, (const struct sockaddr *)&Addr, sizeof(Addr)) != 0) {
			close(*sock);
			*sock = INVALID_SOCKET;
		}
	}
	if (*sock == INVALID_SOCKET) {
		printf("open client %s: Failure to open socket\n", name);
	}
	else {
		printf("open client %s: opened socket %s port %i\n", name, ip, port);
	}
}


static void close_remote_sound_socket(SOCKET * sock, char * name)
{
	if (*sock != INVALID_SOCKET) {
		close(*sock);
		*sock = INVALID_SOCKET;
#ifdef MS_WINDOWS
		WSACleanup();
#endif
		printf("%s: closed socket\n", name);
	}
	else {
		printf("%s: socket already closed\n", name);
	}
}

// start running UDP remote sound on control_head ...
// ... receive radio sound from remote_radio, send mic sound to remote_radio
PyObject * quisk_start_control_head_remote_sound(PyObject * self, PyObject * args)
{
	int radio_sound_port;
	int mic_sound_port;
	int sndsize = 48000;
	char * remote_radio_ip;	// IP address of far end
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, "sii", &remote_radio_ip, &radio_sound_port, &mic_sound_port))
		return NULL;

	name = "radio sound from remote_radio";
	sock = &radio_sound_from_remote_radio_socket;
	open_remote_sound_client(sock, remote_radio_ip, radio_sound_port, sndsize, name);

	name = "mic sound to remote radio";
	sock = &mic_sound_to_remote_radio_socket;
	open_remote_sound_server(sock, remote_radio_ip, mic_sound_port, sndsize, name);

	packets_sent = 0;
	packets_recd = 0;

	return Py_None;
}

// stop running UDP remote sound on control_head
PyObject * quisk_stop_control_head_remote_sound(PyObject * self, PyObject * args)
{
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, ""))
		return NULL;

	name = "radio sound from remote_radio";
	sock = &radio_sound_from_remote_radio_socket;
	close_remote_sound_socket(sock, name);

	name = "mic sound to remote radio";
	sock = &mic_sound_to_remote_radio_socket;
	close_remote_sound_socket(sock, name);

	sound_from_remote_socket_started = 0;	// reset for next time
	sound_to_remote_socket_started = 0;

	printf("total packets sent = %i, recd = %i\n", packets_sent, packets_recd);

	return Py_None;
}

// start running UDP remote sound on remote_radio ...
// ... send radio sound to control_head, receive mic sound from control_head
PyObject * quisk_start_remote_radio_remote_sound(PyObject * self, PyObject * args)
{
	int radio_sound_port;
	int mic_sound_port;
	int sndsize = 48000;
	char * control_head_ip;	// IP address of far end
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, "sii", &control_head_ip, &radio_sound_port, &mic_sound_port))
		return NULL;

	name = "radio sound to control_head";
	sock = &radio_sound_to_control_head_socket;
	open_remote_sound_server(sock, control_head_ip, radio_sound_port, sndsize, name);

	name = "mic sound from control_head";
	sock = &mic_sound_from_control_head_socket;
	open_remote_sound_client(sock, control_head_ip, mic_sound_port, sndsize, name);

	packets_sent = 0;
	packets_recd = 0;

	return Py_None;
}

// stop running UDP remote sound on remote_radio
PyObject * quisk_stop_remote_radio_remote_sound(PyObject * self, PyObject * args)
{
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, ""))
		return NULL;

	name = "radio sound to control_head";
	sock = &radio_sound_to_control_head_socket;
	close_remote_sound_socket(sock, name);

	name = "mic sound from control_head";
	sock = &mic_sound_from_control_head_socket;
	close_remote_sound_socket(sock, name);

	sound_from_remote_socket_started = 0;	// reset for next time
	sound_to_remote_socket_started = 0;

	printf("total packets sent = %i, recd = %i\n", packets_sent, packets_recd);

	return Py_None;
}
