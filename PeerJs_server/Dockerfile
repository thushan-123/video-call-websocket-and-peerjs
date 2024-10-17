FROM node:16

WORKDIR /usr/src/app

# install the peerjs
RUN npm install -g peer

EXPOSE 9000

# run peerjs server
CMD ["peer", "--port", "9000", "--key", "peerjs", "--path", "/"]