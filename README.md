MOSAiC - My Open Source Activity Collection
===========================================

MOSAiC is a site for publishing portfolios with a focus on
code and open source participation. A code portfolio
consists of an overview of one's participation in open
source projects and serves as a portal for potential
employers, interested peers, and yourself.

Projects is a living entity, some are active and some are
dormant and a thing of the past. This should be reflected in
a code portfolio, but at the same time we are lazy and want
things automated. So MOSAiC allows you to associate your
portfolio with open source projects to get statistics and
relevant information automatically updated back into your
portfolio. E.g. by showing a graph of one's active
participation in repositories, issue trackers, mailing lists
ect., indicating if you are still actively working on this
project. Single contributions to major projects, such as
bug-reports and patches will not go unnoticed anymore.

[Try it now for yourself on our demo server][mosaic].

MOSAiC consist of two major components:

1. the website itself written in a combination of django, tastyPie and Backbone.js
2. sources providing activity information to the website

Currently, sources are implemented for git and mercurial
repositories, with additional sources (issue trackers,
wikis, code hosting sites) are planned. The website contains
a worklist of sources it want new information from, and each
source can query the website for work. Sources are language
agnostic, as they communicate with the website through HTTP
- in practice they are implemented in Python though.

The website itself focuses on presenting the portfolio as
clearly as possible, while providing a nice in-line editing
mode for updating portfolios. The current version contains
some quirks in the in-line editing implementation, and is a
bit excessive with calls to the REST interface.

This project was written in 48 hours as part of 
[django-dash 2012][dash].

[mosaic]: http://zh246.o1.gondor.io/
[dash]: http://djangodash.com/
