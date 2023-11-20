FROM node:19 as build

ENV NODE_ENV=development

WORKDIR /app

COPY . .

RUN npm install

ENV HOST=0.0.0.0
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
