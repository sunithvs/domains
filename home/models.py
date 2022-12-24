# domains model to add nginx configration for proxy_pass
import os
import re

from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=100)
    proxy_pass = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super(Domain, self).save(*args, **kwargs)
        # if new domain is added then create a new file in sites-enabled else update the existing file
        if not os.path.exists('/etc/nginx/sites-enabled/' + self.domain):
            os.mknod('/etc/nginx/sites-enabled/' + self.domain)
            with open('/etc/nginx/sites-enabled/' + self.domain, 'w') as f:
                f.write('server {\n')
                f.write('    index index.html index.htm index.nginx-debian.html;\n')
                f.write('    server_name ' + self.domain + ';\n')
                f.write('    location / {\n')
                f.write('        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n')
                f.write('        proxy_set_header Host ' + self.domain + ';\n')
                #  if proxypass contains port number user http or https
                if ':' in self.proxy_pass:
                    if 'https' in self.proxy_pass:
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
            with open('/etc/nginx/sites-enabled/' + self.domain, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'proxy_pass' in line:
                        if ':' in self.proxy_pass:
                            if 'https' in self.proxy_pass:
                                lines[i] = '        proxy_pass ' + self.proxy_pass + ';\n'
                            else:
                                lines[i] = '        proxy_pass http://' + self.proxy_pass + ';\n'
                        else:
                            lines[i] = '        proxy_pass https://' + self.proxy_pass + ';\n'
            f.close()
            with open('/etc/nginx/sites-enabled/' + self.domain, 'w') as f:
                f.writelines(lines)
            f.close()
        os.system('service nginx reload')

    def delete(self, *args, **kwargs):
        super(Domain, self).delete(*args, **kwargs)
        os.remove('/etc/nginx/sites-enabled/' + self.domain)
        os.system('service nginx reload')

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name_plural = "Domains"
