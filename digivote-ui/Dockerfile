FROM node:10.15.1-jessie-slim

WORKDIR /usr/src/app
COPY ./app/package.json /usr/src/app
COPY ./app/package-lock.json /usr/src/app
RUN npm config set registry http://registry.npmjs.org/ && npm install

COPY ./app/public /usr/src/app/public
COPY ./app/src /usr/src/app/src
RUN ls

CMD ["npm", "run", "dev"]