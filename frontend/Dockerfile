# Use Node.js as the base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy only package.json and package-lock.json to leverage caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the application code
COPY . .

# Build the application (optional, if you want to serve a production build)
RUN npm run build

# Expose port 3000 for the app
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
