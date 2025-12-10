#
FROM maven:3.9.11-eclipse-temurin-25 AS builder
WORKDIR /app
RUN export DOCKER_BUILDKIT=1
COPY core /app/core
WORKDIR /app/core
RUN mvn clean install -DskipTests
WORKDIR /app
COPY backend-app /app/backend-app
WORKDIR /app/backend-app
RUN mvn clean package -DskipTests
FROM eclipse-temurin:25-jre
WORKDIR /app
COPY --from=builder /app/backend-app/target/app.jar /app/app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]