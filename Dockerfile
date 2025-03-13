# pull official base image
FROM python:3.10


ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update  \
    && apt-get install netcat-traditional -y  \
    && apt-get install -y firefox-esr wget curl xvfb libgtk-3-0 libx11-xcb1 libdbus-glib-1-2 libxt6 gcc bash-completion gettext nano tmux zsh git tree htop neofetch unzip postgresql-server-dev-all python3-dev musl-dev

RUN GECKODRIVER_VERSION=$(curl -sL https://api.github.com/repos/mozilla/geckodriver/releases/latest | \
    grep '"tag_name":' | cut -d'"' -f4) && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz" -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver

# Проверяем установку
RUN firefox --version && geckodriver --version

# install poetry
RUN pip install poetry
#ENV PATH "/root/.local/bin:$PATH"
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev --no-root
COPY ./ $APP_HOME
COPY ./docker-entrypoint.sh .

RUN ["chmod", "+x", "/usr/src/app/docker-entrypoint.sh"]
RUN sed -i 's/\r$//g'  $APP_HOME/docker-entrypoint.sh
RUN chmod +x  $APP_HOME/docker-entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
