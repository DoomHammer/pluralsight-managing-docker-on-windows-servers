FROM mcr.microsoft.com/dotnet/core/sdk:2.1-nanoserver-sac2016 AS build

ADD . /app/

WORKDIR /app

RUN dotnet build --configuration Release

FROM mcr.microsoft.com/dotnet/core/runtime:2.1-nanoserver-sac2016

COPY --from=build C:\\app\\bin\\Release\\netcoreapp2.1\\hello.exe \
  C:\\app\\bin\\Release\\netcoreapp2.1\\hello.dll \
  C:\\app\\bin\\Release\\netcoreapp2.1\\hello.runtimeconfig.json /app/

WORKDIR /app

CMD /app/hello.exe