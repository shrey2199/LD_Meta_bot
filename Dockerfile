FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN cp netrc_sample ~/.netrc
RUN apt install -y curl
RUN curl https://cli-assets.heroku.com/install.sh | sh
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["bot.py"]
ENTRYPOINT ["python3"]
