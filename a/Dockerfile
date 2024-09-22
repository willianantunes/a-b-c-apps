ARG DOTNET_VERSION=8.0
ARG MAIN_PROJECT_SRC=./src

FROM mcr.microsoft.com/dotnet/sdk:$DOTNET_VERSION AS build-env

ARG MAIN_PROJECT_SRC
ARG RUNTIME

WORKDIR /app

# Restores (downloads) all NuGet packages from the main project
COPY ${MAIN_PROJECT_SRC}/*.csproj ${MAIN_PROJECT_SRC}/
RUN dotnet restore --locked-mode ${MAIN_PROJECT_SRC}

COPY . ./

RUN dotnet publish ${MAIN_PROJECT_SRC} -o out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:$DOTNET_VERSION AS runtime

RUN apt-get update && apt-get install -y curl

WORKDIR /app

RUN useradd appuser && chown appuser /app

USER appuser

COPY --chown=appuser --from=build-env /app/out .
COPY --chown=appuser --from=build-env /app/scripts ./scripts/

CMD [ "./scripts/start-web-production.sh" ]
