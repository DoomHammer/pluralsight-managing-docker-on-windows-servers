FROM mcr.microsoft.com/windows/nanoserver:1809 AS front

ADD front/package.json front/yarn.lock front/.yarnrc /app/

WORKDIR /app

RUN curl.exe -o node.zip https://nodejs.org/dist/v14.15.4/node-v14.15.4-win-x64.zip && \
  mkdir "C:\\node" && \
  tar.exe -xf node.zip -C "C:\\node" --strip-components=1

#Add node to PATH
ENV PATH "C:\\node;%PATH%"

RUN npm install -g yarn && yarn

COPY front/ /app/

ENV PUBLIC_URL=/static

RUN npx react-scripts build

FROM mcr.microsoft.com/windows/servercore:1809 as base

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

ENV PYTHON_VERSION 3.8.2
ENV PYTHON_RELEASE 3.8.2

RUN $url = ('https://www.python.org/ftp/python/{0}/python-{1}-amd64.exe' -f $env:PYTHON_RELEASE, $env:PYTHON_VERSION); \
	Write-Host ('Downloading {0} ...' -f $url); \
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
	Invoke-WebRequest -Uri $url -OutFile 'python.exe'; \
	\
	Write-Host 'Installing ...'; \
# https://docs.python.org/3.5/using/windows.html#installing-without-ui
	Start-Process python.exe -Wait \
		-ArgumentList @( \
			'/quiet', \
			'InstallAllUsers=1', \
			'TargetDir=C:\Python', \
			'PrependPath=1', \
			'Shortcuts=0', \
			'Include_doc=0', \
			'Include_pip=0', \
			'Include_test=0' \
		); \
	\
# the installer updated PATH, so we should refresh our local value
	$env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine); \
	\
	Write-Host 'Verifying install ...'; \
	Write-Host '  python --version'; python --version; \
	\
	Write-Host 'Removing ...'; \
	Remove-Item python.exe -Force; \
	\
	Write-Host 'Complete.';

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 20.0.2

RUN Write-Host ('Installing pip=={0} ...' -f $env:PYTHON_PIP_VERSION); \
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
	Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'; \
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		('pip=={0}' -f $env:PYTHON_PIP_VERSION) \
	; \
	Remove-Item get-pip.py -Force; \
	\
	Write-Host 'Verifying pip install ...'; \
	pip --version; \
	\
	Write-Host 'Complete.';

FROM mcr.microsoft.com/windows/nanoserver:1809

COPY --from=base ["Python", "Python"]

USER ContainerAdministrator
RUN setx /M PATH %PATH%;c:\Python\;c:\Python\scripts\;
USER ContainerUser
	
ADD requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD . /app/

ENV PORT=8000

EXPOSE 8000

COPY --from=front /app/build/ /app/static/

CMD python /app/main.py
