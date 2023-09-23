# Second Sight Frontend

This directory holds the Second Sight frontend code. The Frontend is a React project that generates a website to interact with the backend API.

# Building

Before building and running the frontend the backend will need to be running.

You can run the frontend for development with the following commands

```
cd static
npm install
npm start
```

This will build the React site then open it in your web browser automatically.

You can also run `npm run build` to build the static site. This site can be served via the `poetry run second-sight-frontend` command. All the built content exists in the `build` directory.