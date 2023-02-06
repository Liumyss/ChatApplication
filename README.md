# Overview

In this Chat Application, my goal is to make a simple connection between several clients and server. 
It helped me to apply the basics of networking and to know how to apply this in the future in bigger
projects related to networking. I have always been curious about CyberSecurity and understanding 
networking through programming is the reason why I made this software.

To use this server you need to have both the server and client files running. In one computer, you will have to run 
the server file, it will be the foundation of the chatroom that will deal with each connections of the clients. To join
the server, you will need to run the client file in another computer. After creating an username, you will be able 
to access the chatroom. You can repeat the same thing with the client file and other computers connected in the same 
network for this application.

[Software Demo Video](https://youtu.be/zxN-As9UVD4)

# Network Communication

I build the app by following the architecture client/server

I used TCP for this example of a Chat Room. 

The format of the messages send from the server to the clients is "utf-8"

# Development Environment

Visual Studio Code
Terminal

### Language and Libraries Used
* Python
* Sockets, Threading

# Useful Websites

* [Python Socket Server](https://docs.python.org/3.6/library/socketserver.html)
* [Python Socket](https://docs.python.org/3/library/socket.html)
* [What is TCP?](https://www.geeksforgeeks.org/what-is-transmission-control-protocol-tcp/)

# Future Work

* Give users access to create an account with an username and a password that will be saved externally in another file
* Use the hashing library for passwords saved from the chat server
* Create a GUI for the chat app