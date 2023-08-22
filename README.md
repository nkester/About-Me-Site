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
  * [Conatiner Image](#container-image)  
  * [Local Development](#local-development)  
  * [Build a New `Academic` Themed Hugo Site](#build-a-new-academic-themed-hugo-site)  
  * [Connect to Google Firebase](#connect-to-google-firebase)  
  * [Employ GitOps: GitLab CI to Google Firebase](#employ-gitops-gitlab-ci-to-google-firebase)  
  * [Enable temporary Firebase Preview Channels](#preview-channel)  

## Site Content  

## Site Deployment  

### Container Image  

In order to build the hugo site and push it to Google Firebase Hosting, I created my own container image. I use this container image within my GitLab CI Pipeline but have applied the same steps to my personal VS Code development container to have similar capabilities during development.  

This container image is stored within this project's Container Registery and is rebuilt only when the `hugo_dockerfile` changes on the `main` branch.

The container currenly uses a Ubuntu-22.04 base image and installs the Google Firebase CLI, Hugo, Golang, and Python 3. In the near future I will update the base image to either UBI8 or Alpine to make the resulting container image smaller.  

#### Docker File Explained  

The dockerfile that specifies this container image build sequence is named `hugo_dockerfile`.  

It is based on the official Ubuntu 22.04 (Jammy Jellyfish) container image and contains six build steps.  

**Build Step 1 - System**  

The base Ubuntu image is minimal so I first start by updating the package repo and upgrading all possible packages. Then I install `curl` and `git` which allows me to install other tools in future build steps.  

**Build Step 2 - Google Firebase CLI**  

Navigate to the `/tmp/` folder and use `curl` to download the latest version of Google's Firebase CLI tools from Google.  

**Build Step 3 - Hugo Extended**  

Navigate to the `/tmp/` folder and use `curl` to download hugo-extended from github. The `Academic` theme requires `hugo extended` rather than base `hugo` to build.  

This download uses the environment variable set in line 4 of the dockerfile: `ENV HUGO_VERSION`. At this time it is version `0.100.2`. `gohugoio` names is binaries in a consistent manner so the docker file builds the version into the binary file name format and saves it as the `HUGO_BINARY` environment variable.  

This `HUGO_BINARY` env is passed to the curl command to download the desired version of hugo.  

The dockerfile then uses `dpkg` to install that hugo binary package.  

**Build Step 4 - Go**  

The `Academic` theme also requires that Golang (a.k.a Go) is installed. I have not found a requirement for specific or super recent versions so I'll use the version of golang available in the `apt-get` repo.  

In the future I may need to update this to pull a specific version.  

**Build Step 5 - Python**  

Install python 3 and pip to support the `get_preview_url.py` script used in the GitLab CI process. Currently I only use base python modules so there is no need to install additional modules.  

**Build Step 6 - Clean Up**  

In order to keep the container image as small as possible, this step removes everthing that was downloaded to the `/tmp/` directory and clears all downloaded archive files.

#### Accessing the Container Image  

The container registry this image is stored in is: `registry.gitlab.com/nkester/about-me-site/hugo_build`.  

Each image is tagged with the git short commit SHA that corresponds to the commit that ran the build pipeline.  

Additionally, I use floating tags so I can always access the most recent container image built on a branch. These floating tags correspond to the branch name. Therefore, the latest container image built on the production branch (`main`) is located at: `registry.gitlab.com/nkester/about-me-site/hugo_build:main`.  
 
#### References  

  * As a guide I used [marzouka's container image](https://github.com/marzouka/docker-hugo-firebase/blob/master/Dockerfile) stored in GitHub.  
  * I also used the [Google Firebase documentation](https://firebase.google.com/docs/cli#install_the_firebase_cli) to install and use the firebase cli.  
  * The GitLab docs on the GitLab-CI syntax is helpful, [specifically the section on rules](https://docs.gitlab.com/ee/ci/yaml/#rules).  
  * [How to install Golang on Ubuntu-22.04](https://linuxconfig.org/how-to-install-go-on-ubuntu-22-04-jammy-jellyfish-linux)  
  * **Future Work for installing specific versions** [Installing Golang](https://go.dev/doc/install)  

### Local Development  

I used the VSCode container I normally develop in for this purpose as well. In order to serve the website locally, however, we need to expose additional ports when the container starts.  

My base VS Code container image does not include the Google firebase, Hugo, and GoLang dependencies required to develop this site. To support local development I've extended my base VS Code container image using the `dev-ide_dockerfile`. This is simply the same dockerfile specifications as is used to build and deploy the site but I use my VS Code container as the base.  

Additionally, I save container image to this project's container registry through the `.gitlab-ci.yaml` specification to the `registry.gitlab.com/nkester/about-me-site/dev_ide` container registry. 

Run this container image with the additional ports exposed with the following `podman` command.  

` podman run --rm -d -p 8083:8443 -p 1313:1313 -e PUID=1000 -e PGID=1000 -e TZ=America/New_York -e PASSWORD=mypass -e SUDO_PASSWORD=mypass -v neil-work:/config --name hugo registry.gitlab.com/nkester/about-me-site/dev_ide:develop`  

#### Serve the New Site Locally 

`hugo server --bind "0.0.0.0"` 

The `--bind` flag allows to see the served site outside of the container at the default `1313` port.  

I can then navigate to `localhost:1313` on my local computer to see the site served from my local VS Code development container.  

### Build a New `Academic` Themed Hugo Site  

While I tried to add the theme as a hugo module, I ran into issues removing the examples provided in the demo site. I'll include those steps at the end of this section so I can try again later but in the mean time I went with the approach of cloning the template project.  

#### 1. Clone the template project  

First, fork the theme's GitHub project or import it into a GitLab project. Do not enable mirroring.  

Test the site builds properly with `hugo serve --bind "0.0.0.0"`. This command allows us to serve the website from within my VSCode container exposed on port 1313.  

#### 2. Update the `config.yaml` file  

The [hugo configuration documentation](https://gohugo.io/getting-started/configuration/) does a good job describing how to organize configuration files. **I have not yet implemented different configurations for `development` and `production` environments.**  

Navigate to `./config/_default/` to find the configuration files. This is where we can change our front matter and other parameters.  

#### 3. Get to Work  

This is the starting point from which I can now begin updating content, adding my own widgets, and customizing the site.

#### XX. Using Hugo Modules for the Theme  

Using Hugo modules allows us to loosely couple my project with the work accomplished by the theme's developers. This approach worked beautifully except for the fact that the `Academic` theme module includes all of the content provided for the demo site. Because those files are packaged up and I found no parameter to pass for ignore them, I was unable to edit or delete that content.  

**Step 1. Make your Project a Hugo Module**  

`hugo mod init <project name>`  

**Step 2. Specify Modules to Import**  

In your `config.yaml` file, add a stanza describing which hugo modules to import into your new module.  

That stanza should look like this:  

```yaml
module:
  imports:
    # Project Theme
    - path: "github.com/wowchemy/starter-hugo-academic"
```  

As described in the `Using Modules` article listed below, I've provided a comment on what that module import is for.  

**Step 3. Pull in that Module Dependency**  

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
**Step 4. Serve the Website**  

Now we can serve the website as normal with `hugo serve --bind "0.0.0.0"`  

The "vendor" command allows you to see what the contents of your site look like. Executing `hugo mod vendor` pulls in all of the files in the imported modules and places them in the `_vendor` directory. We can delete this directory when we are done looking at it.  

> **The hosted vCard**: I have provided a vCard (vcf file) in the `/static/uploads` directory. It is built by `makevcard.py` in the project's root directory. This does not re-build automatically so the python script needs to be re-run if changed. This does not, yet, pull from information in this site's `Contact` section but it should. If updating one, ensure to update the other until they are connected.  

#### References:  

  * **VERY USEFUL** [Using Modules](https://www.hugofordevelopers.com/articles/master-hugo-modules-managing-themes-as-modules/)  
  * Fix for security issue when building [GitHub](https://github.com/wowchemy/wowchemy-hugo-themes/discussions/2559#discussioncomment-1840591)  


### Connect to Google Firebase  

  > This assumes you have already created a Firebase CLI CI Token and stored it in the project's GitLab CI Variables section under the variable name `FIREBASE_TOKEN`. Do this by following the steps in Reference 1 of this section.  

Execute these steps in the VS Code container I ran in the previous step or your own development environment.  

#### Initializing the firebase project  

navigate to the site's project directory and execute the terminal command: `firebase init --token <your token>`. This approach uses the CI token we generated previously. I've used this option so that I don't need to authenticate with google every time.  

When you run this command, it will ask several questions. These were my reponses: 
  1. Creating a hosting service only  
  2. Use an existing project (I had already create a firebase project through the Firebase UI).  
    a. This then gave me the option of which existing project I wanted to use.  
  3. Firebase asks what directory to use as your public directory. Hugo has already created a directory for us named `public` so we will use that. Respond to this question with `public`.  
    a. The workflow will look like this: You add files to your hugo template in this GitLab project, hugo will then build those files into a static site and place those artifacts (results of the build process) in the `public` folder. Firebase will then deploy the contents of the `public` folder to Google's servers to be hosted.  
  4. Firebase asks if I want to configure this as a single-page app. **I don't know but at this time I selected `N`**.  
  5. I am using GitLab instead of GitHub so I selected `N` when asked to set up automatic build and deploys with GitHub.  

#### Connect Your Firebase Project to your Domain  

In order to do this, first get the information from your Firebase Project required to set up an `A` name in your domain record. This should be an option you can select from the Firebase GUI and should be under the `Easy` setup option, not the `Advanced`. It is simply the IPv4 address to your Firebase project hosted app.  

Add a new domain record with your domain registry, request a new `A` record, and provide that IPv4. It may take some time to update but that should be all you need for a basic `http` site. 

#### References  

  1. This reference from the Google Docs walks you through setting up the Firebase CLI in a headless continuous integration (CI) environment [here](https://firebase.google.com/docs/cli#cli-ci-systems).  
  
  2. Other information on the firebase CLI is [here](https://firebase.google.com/docs/cli#sign-in-test-cli).

### Employ GitOps: GitLab CI to Google Firebase  

Implementing Automatic Builds and Deploys to Firebase through Google CI  

Pre-requisites:  

  1. Now that we have the components: 1) `FIREBASE_TOKEN` in the GitLab project, 2) Firebase project initialized within the file structure of the GitLab project, 3) A container image that a GitLab Runner can execute to perform our operations, and 4) A domain name record that connects your domain name to the firebase hosting project. I used a subdomain off of my name `nkester.com` domain that I own.  

  2. As described previously, ensure the `FIREBASE_TOKEN` CI Variable is not "Protected" until you are ready to add this workflow to apply only to protected branches (a `develop` and `main` branch for instance).  

#### GitLab CI `.gitlab-ci.yaml` File  

This file describes all of the triggers that will initiate the GitLab CI pipelines, how those pipelines are organized, and what each job does.  

For this project I have organized the pipeline into three stages: `build`, `preview`, and `publish`.  

All jobs in this `yml` are set up as merge triggers so they only execute when a feature branch has a merge request into a protected branch (`main` or `develop`).  

**`build`**  

The `build` stage only has one job and is meant to build new container images, tag them appropriately, and store them in the project's container image registry.  

To minimize un-needed build events, this job only triggers when the commit branch is either `main` or `develop` AND the `hugo_dockerfile` file has changed.  

I have, however, retained the ability to execute this job manually if needed. This is useful when I want to pull in recent patches to the base container but the original dockerfile did not change. 

Ensure the `environment.url` argument of the `.gitlab-ci.yml` is accurate. Also, ensure the `only` stanza indicates the correct branch you want this to execute on.  

**`preview`**  

The `preview` stage has one job and is meant to build the hugo site from the `develop` branch and deploy it to a temporary Google Firebase Hosting Preview Channel.  

After the job builds the hugo site, it pushes it to the `develop` Google Firebase channel with a specification that the resulting dynamic URL only lives for 1 hour.  

The job then uses the `get_preview_url.py` script I made to parse the json response from the firebase_cli to extract the dynamic preview url. Finally, it applies this URL to the `review/develop` GitLab environment that is accessible from the project's GitLab UI.  

Access the GitLab Environments [here](https://gitlab.com/nkester/about-me-site/-/environments)

**`publish`**  

The `publish` stage has one job and is meant to build the hugo site from the `main` branch and deploy it to production Google Firebase channel.  

#### References  

  * [GitLab Dynamic Environment URLs](https://docs.gitlab.com/ee/ci/environments/#example-of-setting-dynamic-environment-urls)  
  * [Firebase Reference Documentation](https://firebase.google.com/docs/hosting/manage-hosting-resources?authuser=0&hl=en)    * https://www.freecodecamp.org/news/hugo-firebase-how-to-create-your-own-dynamic-website-for-free-in-minutes-463b4fb7bf5a/  
  * [hugo to firebase with gitlab ci](https://iyadmarzouka.com/post/how-to-deploy-a-hugo-site-to-firebase-using-gitlab-cicd/)  
