# Autopile
## This is auto compile scripts writen for auto test

---

There are 3 .py files
> 1. ./autopile.py
> 2. ./ap_email.py
> 3. ./ap_config.py
---


For I used pipenv.

run 

```shell
pip3 install pipenv
pipenv install --dev
```
to build environment and
```shell
pipenv shell
```
to active the environment

---



### Usages :

> Modify the configure in ap_config.py and run autopile.py

---

### Configure in ap_config.py

**repository** 
> The repo's url

**projectname**
> The name of the directory created when git clone

**globalCwd** 
> The main directory

**thread** 
> number of threads used in make

**maxTryTimes**
> Maximum retry times, if it is reached, the autopile will fail with e-mail sent to admins.

**receivers**
> Administrator's e-mail addresses










