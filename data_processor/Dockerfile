# Multi stage build
FROM rust:1.64 as build

RUN USER=root cargo new --bin holodeck
WORKDIR /job

COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml
COPY ./src ./src

RUN cargo build --release


FROM debian:buster-slim

COPY --from=build /job/target/release/data-processor-sample .

CMD ["./data-processor-sample"]
