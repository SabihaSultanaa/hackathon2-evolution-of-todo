FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the project
RUN npm run build

EXPOSE 3000

# Start the Next.js server
CMD ["npm", "start"]