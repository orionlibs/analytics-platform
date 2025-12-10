# Detail on duplicating this repository


In lieu of a fork, you can duplicate this repository using the following steps:



0. Setup ssh access to github (https://docs.github.com/en/authentication/connecting-to-github-with-ssh)


1. Create an empty repository on github using the "gh" cli (or via the githubweb interface)

```
gh repo create git@github.com:${YOUR_GITHUB_USERNAME}/new-deploy-otel-demo-alloy-copy --private 
```

2. Create a "bare" clone of this repostitory 

```
cd /tmp
git clone --bare git@github.com:grafana/deploy-otel-demo-alloy
```

3. cd into the bare clone directory

```
cd /tmp/deploy-otel-demo-alloy.git
```

4. Push the bare clone to the new repo

```
git push --mirror git@github.com:${YOUR_GITHUB_USERNAME}/new-deploy-otel-demo-alloy-copy.git
```

5. Clean up the bare clone

```
rm -rf /tmp/deploy-otel-demo-alloy.git
```


6. create a new repository directory and clone the new repository

```
mkdir -p ~/github/${YOUR_GITHUB_USERNAME}
cd ~/github/${YOUR_GITHUB_USERNAME}
git clone git@github.com:${YOUR_GITHUB_USERNAME}/new-deploy-otel-demo-alloy-copy.git
```



7. Profit!

