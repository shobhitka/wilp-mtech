FROM yiisoftware/yii2-php:8.0-apache
WORKDIR /webapp
COPY webapp.sh /usr/bin
RUN git clone https://github.com/shobhitka/crb-checker.git && cd crb-checker && composer install
EXPOSE 8080
CMD /usr/bin/webapp.sh

