#include "../headers/goggle-bot.h"
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>

int bot_connect();

int main(int argc, char **argv){
  /*
   * TODO: Create bot that can communicate with automatic goggles
   * in a unique way. That allows for more advanced techniques such
   * as privilege escalation.
   */

  /*
   * NOTE: Capabilities:
   *  -- Will need parser to understand commands over the network
   *   1.) Basic enumeration
   *   2.) Basic privilege escalation capabilities
   *   3.) Create persistence. 
   */

	char *host;
	int port;

	if(argc != 3){
		printf("Usage: %s <ip> <port>\n", argv[0]);
		exit(0);
	}

	host = argv[1];
	port = atoi(argv[2]);

	printf("I am test-bot, fear me.\n");
	printf("Host: %s\nPort:%d\n", host, port);
  	return 0;
}

