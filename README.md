# My Website

This project serves two purposes for me.  

  * First, it produces an easily accessible and dynamic portfolio, resume and cirruculum vitae (CV) of my work as a leader, data scientist, and technologist. Through this I will link to publically shareable work to demonstrate my capabilities and past experiences.  

  * Second, it provides me further practice and experience integrating GitLab Continuous Integration / Continuous Delivery (CI/CD) actions with building and managing software container images, content delivery to Google Cloud Platform (GCP) resources such as Firebase Hosting, and practice implementing GitOps.  

## The Site  

The foundation of this site comes from the [Hugo](https://gohugo.io/getting-started/quick-start/) `Academic` Theme which I cloned from the [wowchemy academic GitHub project](https://github.com/wowchemy/starter-hugo-academic). Wowchemy also provides a [demonstration of the base academic site](https://academic-demo.netlify.app/).  

The theme referenced above was meant to deploy into `netlify` automatically through GitHub Actions. This did not align with my previously stated project purpose so I altered the deployment model.  

For that reason I broke this documentation into two primary sections, one explaining the site's content and another describing the mechanisms that enable me to build and deploy the site through GitLab powered GitOps.  

Below is a table of contents for items in both sections:  

[Site Content](#site-content)  
  * None  
[Site Deployment](#site-deployment)  
  * [Preview Channel](#preview-channel)

## Site Content  

## Site Deployment  

### Preview Channel

Changes to the develop branch deploys a preview of the site that lives for one hour.  

This is set up in a `review/deploy` GitLab environment. It runs automatically at commit on the `develop` branch or manually through the GitLab UI.  

Access the GitLab Environments [here](https://gitlab.com/nkester/about-me-site/-/environments)  

In order to extract the Google Firebase Preview Channel URL from the Firebase CLI response I wrote a simple python script named: `get_preview_url.py`.  

### References  

  * [GitLab Dynamic Environment URLs](https://docs.gitlab.com/ee/ci/environments/#example-of-setting-dynamic-environment-urls)  
  * [Firebase Reference Documentation](https://firebase.google.com/docs/hosting/manage-hosting-resources?authuser=0&hl=en)

## Hugo Theme  

### References  

  * https://www.freecodecamp.org/news/hugo-firebase-how-to-create-your-own-dynamic-website-for-free-in-minutes-463b4fb7bf5a/  
  * [hugo to firebase with gitlab ci](https://iyadmarzouka.com/post/how-to-deploy-a-hugo-site-to-firebase-using-gitlab-cicd/)  

# Hugo Container Build  

This container will serve as my vehicle to build the website from the source files in this project and deploy it to the Google Firebase Project I've set up to host my site.  

This container image is stored within this project's Container Registery and is rebuilt only when the `hugo_dockerfile` changes on the `main` branch.

The container currenly has a Ubuntu-22.04 base image, the Google Firebase CLI, Hugo, and Golang installed. In the near future I will update the base image to be either UBI8 or Alpine to make the resulting container image smaller.  

## Docker File Explained  

The dockerfile that specifies this container image build sequence is named `hugo_dockerfile`.  

It is based on the official Ubuntu 22.04 (Jammy Jellyfish) container image and contains six build steps.  

### Build Step 1 - System  

The base Ubuntu image is minimal so I first start by updating the package repo and upgrading all possible packages. Then I install `curl` and `git` which allows me to install other tools in future build steps.  

### Build Step 2 - Google Firebase CLI  

Navigate to the `/tmp/` folder and use `curl` to download the latest version of Google's Firebase CLI tools from Google.  

### Build Step 3 - Hugo Extended  

Navigate to the `/tmp/` folder and use `curl` to download hugo-extended from github. The **"Academic"** theme requires `hugo extended` rather than base `hugo` to build.  

This download uses the environment variable set in line 4 of the dockerfile: `ENV HUGO_VERSION`. At this time it is version `0.100.2`. `gohugoio` names is binaries in a consistent manner so the docker file builds the version into the binary file name format and saves it as the `HUGO_BINARY` environment variable.  

This `HUGO_BINARY` env is passed to the curl command to download the desired version of hugo.  

The dockerfile then uses `dpkg` to install that hugo binary package.  

### Build Step 4 - Go  

The **"Academic"** theme also requires that Golang (a.k.a Go) is installed. I have not found a requirement for specific or super recent versions so I'll use the version of golang available in the `apt-get` repo.  

In the future I may need to update this to pull a specific version.  

### Build Step 5 - Python  

Install python 3 and pip to support the `get_preview_url.py` script used in the GitLab CI process. Currently I only use base python modules so there is no need to install additional modules.  

### Build Step 6 - Clean Up

In order to keep the container image as small as possible, this step removes everthing that was downloaded to the `/tmp/` directory and clears all downloaded archive files.

### Accessing the Container Image  

The container registry this image is stored in is: `registry.gitlab.com/nkester/about-me-site/hugo_build`.  

Each image is tagged with the git short commit SHA that corresponds to the commit that ran the build pipeline.  

Additionally, I use floating tags so I can always access the most recent container image built on a branch. These floating tags correspond to the branch name. Therefore, the latest container image built on the production branch (`main`) is located at: `registry.gitlab.com/nkester/about-me-site/hugo_build:main`.  
 

## References  

  * As a guide I used the container image created by [marzouka here](https://github.com/marzouka/docker-hugo-firebase/blob/master/Dockerfile).  
  * I also used the Google Firebase documentation located in their docs [here](https://firebase.google.com/docs/cli#install_the_firebase_cli).  
  * The GitLab docs on the GitLab-CI syntax is helpful, specifically the section on rules located [here](https://docs.gitlab.com/ee/ci/yaml/#rules).  
  * [How to install Golang on Ubuntu-22.04](https://linuxconfig.org/how-to-install-go-on-ubuntu-22-04-jammy-jellyfish-linux)  
  * **Future Work for installing specific versions** [Installing Golang](https://go.dev/doc/install)  

# Build a new Hugo site  

While I tried to add the theme as a hugo module, I ran into issues removing the examples provided in the demo site. I'll include those steps at the end of this section so I can try again later but in the mean time I went with the approach of cloning the template project.  

## 1. Clone the template project  

We can do this a few ways. The first is to fork the theme's GitHub project or import it into a GitLab project and then break the fork relationship or do not enable mirroring. This probably makes the most sense but I didn't want to lose the commits I had already made to this project.  

Another option, the one I used in this case, is to clone the theme's GitHub project to another folder and copy over the files required to run the site.  

Test the site builds properly with `hugo serve --bind "0.0.0.0"`. This command allows us to serve the website from within my VSCode container exposed on port 1313.  

## 2. Update the `config.yaml` file  

The hugo configuration documentation [here](https://gohugo.io/getting-started/configuration/) goes a good job describing how to organize configuration files. **I have not yet implemented different configurations for `development` and `production` environments.**  

Navigate to `./config/_default/` to find the configuration files. This is where we can change our front matter and other parameters.  


## XX. Using Hugo Modules for the Theme  

Using Hugo modules allows us to loosely couple my project with the work accomplished by the theme's developers. This approach worked beautifully except for the fact that the `Academic` theme module includes all of the content provided for the demo site. Because those files are packaged up and I found no parameter to pass for ignore them, I was unable to edit or delete that content.  

### Step 1. Make your Project a Hugo Module  

`hugo mod init <project name>`  

### Step 2. Specify Modules to Import  

In your `config.yaml` file, add a stanza describing which hugo modules to import into your new module.  

That stanza should look like this:  

```yaml
module:
  imports:
    # Project Theme
    - path: "github.com/wowchemy/starter-hugo-academic"
```  

As described in the `Using Modules` article listed below, I've provided a comment on what that module import is for.  

### Step 3. Pull in that Module Dependency  

Now that we've added the theme module to out `config.yaml` we need to pull it in with:  

`hugo mod get`  

  > **Note:** I got an error when I did this regarding some security issues. This is a known issue that is addressed in my second reference in this section. Deal with it by adding the following stanza to your `config.yaml` file.  

```yaml
security:
  funcs:
    getenv:  
      - "^HUGO_"
      - "^WC_"
```
### Step 4. Serve the Website  

Now we can serve the website as normal with `hugo serve --bind "0.0.0.0"`  

The "vendor" command allows you to see what the contents of your site look like. Executing `hugo mod vendor` pulls in all of the files in the imported modules and places them in the `_vendor` directory. We can delete this directory when we are done looking at it.  

### References:  

  * **VERY USEFUL** [Using Modules](https://www.hugofordevelopers.com/articles/master-hugo-modules-managing-themes-as-modules/)  
  * Fix for security issue when building [GitHub](https://github.com/wowchemy/wowchemy-hugo-themes/discussions/2559#discussioncomment-1840591)  

# Local development (not headless)  

I used the VSCode container I normally develop in for this purpose as well. In order to serve the website locally, however, we need to expose additional ports when the container starts. I used the following `podman` command for this.  

` podman run --rm -d -p 8083:8443 -p 1313:1313 -e PUID=1000 -e PGID=1000 -e TZ=America/New_York -e PASSWORD=mypass -e SUDO_PASSWORD=ennser83 -v neil-work:/config --name hugo registry.gitlab.com/nkester-personal-cloud/containers/linuxserver-vscode/temp:latest`  

I then ran the same commands in the VSCode terminal as I have in the `hugo_dockerfile` in order to install `hugo` and `golang`.  

## Serve the new site  

`hugo server --bind "0.0.0.0"` 

The `--bind` flag allows to see the served site outside of the container at the default `1313` port.

# Connect to Google Firebase  

  > This assumes you have already created a Firebase CLI CI Token and stored it in the project's GitLab CI Variables section under the variable name `FIREBASE_TOKEN`. Do this by following the steps in Reference 1.  

Execute these steps in the VS Code container I ran in the previous step or your own development environment.  

## Initializing the firebase project  

navigate to the site's project directory and execute the terminal command: `firebase init --token <your token>`. This approach uses the CI token we generated previously. I've used this option so that I don't need to authenticate with google every time.  

When you run this command, it will ask several questions. These were my reponses: 
  1. Creating a hosting service only  
  2. Use an existing project (I had already create a firebase project through the Firebase UI).  
    a. This then gave me the option of which existing project I wanted to use.  
  3. Firebase asks what directory to use as your public directory. Hugo has already created a directory for us named `public` so we will use that. Respond to this question with `public`.  
    a. The workflow will look like this: You add files to your hugo template in this GitLab project, hugo will then build those files into a static site and place those artifacts (results of the build process) in the `public` folder. Firebase will then deploy the contents of the `public` folder to Google's servers to be hosted.  
  4. Firebase asks if I want to configure this as a single-page app. **I don't know but at this time I selected `N`**.  
  5. I am using GitLab instead of GitHub so I selected `N` when asked to set up automatic build and deploys with GitHub.  

## Connect Your Firebase Project to your Domain  

In order to do this, first get the information from your Firebase Project required to set up an `A` name in your domain record. This should be an option you can select from the Firebase GUI and should be under the `Easy` setup option, not the `Advanced`. It is simply the IPv4 address to your Firebase project hosted app.  

Add a new domain record with your domain registry, request a new `A` record, and provide that IPv4. It may take some time to update but that should be all you need for a basic `http` site. 

## References  

  1. This reference from the Google Docs walks you through setting up the Firebase CLI in a headless continuous integration (CI) environment [here](https://firebase.google.com/docs/cli#cli-ci-systems).  
  
  2. Other information on the firebase CLI is [here](https://firebase.google.com/docs/cli#sign-in-test-cli).

# Implementing Automatic Builds and Deploys to Firebase through Google CI  

Now that we have the components: 1) `FIREBASE_TOKEN` in the GitLab project, 2) Firebase project initialized within the file structure of the GitLab project, 3) A container image that a GitLab Runner can execute to perform our operations, and 4) A domain name record that connects your domain name to the firebase hosting project. I used a subdomain off of my name `nkester.com` domain that I own.  

Ensure the `environment.url` argument of the `.gitlab-ci.yml` is accurate. Also, ensure the `only` stanza indicates the correct branch you want this to execute on.  

As described previously, ensure the `FIREBASE_TOKEN` CI Variable is not "Protected" until you are ready to add this workflow to apply only to protected branches (a `develop` and `main` branch for instance). 
  
