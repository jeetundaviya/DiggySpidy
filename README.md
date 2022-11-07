<h1><b>Diggy Spidy</b></h1>
<img src="https://user-images.githubusercontent.com/56348104/190194186-f85ea513-227c-424f-9ee6-47f649b33595.png">
<h3><b>[Q] What is Diggy Spidy ?</b></h3>

<h3><b>[A] Diggy Spidy is a Surface and a Dark Web Crawler.</b></h3>

<h5><b>[*] (Method 1) Installation :-</b></h5>

<code>git clone https://github.com/jeetundaviya/DiggySpidy.git</code>

<code>cd DiggySpidy</code>

<code>pip install -r requirements.txt</code>

<h5><b>[*] (Method 2) Installation by Docker :-</b></h5>

<code>git clone https://github.com/jeetundaviya/DiggySpidy.git</code>

<code>cd DiggySpidy</code>

<code>docker-compose run DiggySpidy</code>

<h5><b>[*] (Method 3) Installation from <a href="https://hub.docker.com/repository/docker/jeetundaviya/diggy-spidy">Docker Hub</a></b></h5>

<h5><b>[*] Usage :-</b></h5>

<code>python diggy-spidy.py</code>

<h5><b>[*] Features :-</b></h5>

-> Slow and Fast Mode.<br>
-> Takes Full-Screenshots of website for future analysis.<br>
-> Website Domain Specific Crawling.<br>
-> Crawling Depth Control.<br>
-> Keyword Based Filter for the textual data found on the website. (Keyword matches found from the text content found on the website)<br>
-> Stopwords and Must have words filter in the link.<br>
-> Multiple List Crawling (Parallel Crawling)<br>

<h5><b>[*] Special :-</b></h5>

1) Keyword Based Fetching Links :-

-> We have made custom list of the various sources (search-engines,public forums,public datasets,etc) and have made custom scripts for the each source which is able to scrap the results from it. (Expending the Sources List for collection of larger data)

2) Locating Found Text in Screenshots and Highlighting it for the keyword filter for matches found ! (Under Development)
	
<h5><b>[*] Our Goal :-</b></h5>

-> We aim to develop a cyber-surveillance and cyber-threat-intelligence model from our updated indexed dataset and also to built an alert system if any of the requested target is about to compromise from our model.