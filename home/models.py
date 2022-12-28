# domains model to add nginx configration for proxy_pass
import os
import re

from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SubDomain(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    proxy_pass = models.CharField(max_length=100)

    @property
    def domain_name(self):
        return self.name + '.' + self.domain.name

    class Meta:
        unique_together = ('domain', 'name')
        verbose_name_plural = 'Sub Domains'

    def add_ssl(self):
        "this will run certbot command to add ssl to the domain"
        os.system('certbot --nginx -d ' + self.domain_name)

    def save(self, *args, **kwargs):
        super(SubDomain, self).save(*args, **kwargs)
        # if new domain is added then create a new file in sites-enabled else update the existing file
        if not os.path.exists('/etc/nginx/sites-enabled/' + self.domain_name):
            os.mknod('/etc/nginx/sites-enabled/' + self.domain_name)
            with open('/etc/nginx/sites-enabled/' + self.domain_name, 'w') as f:
                f.write('server {\n')
                f.write('    index index.html index.htm index.nginx-debian.html;\n')
                f.write('    server_name ' + self.domain_name + ';\n')
                f.write('    location / {\n')
                f.write('        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n')
                f.write('        proxy_set_header Host ' + self.domain_name + ';\n')
                #  if proxypass contains port number user http or https
                if ':' in self.proxy_pass:
                    if 'http' in self.proxy_pass:
                        f.write('        proxy_pass ' + self.proxy_pass + ';\n')
                    else:
                        f.write('        proxy_pass http://' + self.proxy_pass + ';\n')
                else:
                    f.write('        proxy_pass https://' + self.proxy_pass + ';\n')
                f.write('        proxy_redirect off;\n')
                f.write('        proxy_set_header Upgrade $http_upgrade;\n')
                f.write('        proxy_set_header Connection "upgrade";\n')
                f.write('    }\n')
                f.write('}\n')
            f.close()
        else:
            raise Exception('Domain cant be updated')
        os.system('service nginx reload')
        self.add_ssl()

    def delete(self, *args, **kwargs):
        super(SubDomain, self).delete(*args, **kwargs)
        os.remove('/etc/nginx/sites-enabled/' + self.domain_name)
        os.system('service nginx reload')

    def __str__(self):
        return self.domain_name
