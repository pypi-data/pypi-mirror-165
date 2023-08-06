# Website Classification API

Python3 client library for [Website Classification](https://www.websitecategorizationapi.com). 

Website classification API s a python library that allows to classify websites based on IAB and E-commerce taxonomies. 

## Installation 
```
pip install websiteclassificationapi
```
## Requirements

Only Python 3 is supported. You need an API key which you can obtain at . 
Python library requires only requests package. 

## Documentation 

More detailed API documentation is [available here](https://www.websitecategorizationapi.com/api.php). 

## Examples 

```
from websiteclassificationapi import websiteclassificationapi

api_key = 'h2XurA' # you can get API key from www.websitecategorizationapi.com
url = 'www.alpha-quantum.com' # can be set to any valid URL
classifier_type = 'iab1' # should be set to either iab1 (Tier 1 categorization) or iab2 (Tier 2 categorization) for general websites or ecommerce1, ecommerce2 and ecommerce3 for E-commerce or product websites

# calling the API
print(websiteclassificationapi.get_categorization(url,api_key,classifier_type))
```

## How to select classifiers of different taxonomies

Classifier_type should be set to either iab1 (Tier 1 categorization) or iab2 (Tier 2 categorization) for general websites or ecommerce1, ecommerce2 and ecommerce3 for E-commerce or product websites. 

IAB Tier 1 categorization returns probabilities of text being classified as one of 29 possible categories.

IAB Tier 2 categorization returns probabilities of text being classified as one of 447 possible categories.

Ecommerce Tier 1 categorization returns probabilities of text being classified as one of 21 possible categories.

Ecommerce Tier 2 website categorization returns probabilities of text being classified as one of 182 possible categories.

Ecommerce Tier 3 website categorization returns probabilities of text being classified as one of 1113 possible categories.

## Taxonomies

You can find more information about IAB taxonomy at this page: https://www.iab.com/guidelines/content-taxonomy/. 

## AI explainability

One of the unique features of classifiers is that they provide machine learning interpretability or artificial intelligence explainability (XAI) in the form of words that most contribute to resulting classification. 

Example 1 of explainability: 
![Image1](https://www.websitecategorizationapi.com/product_categorization.png)

Example 2 of explainability: 
![Image1](https://www.websitecategorizationapi.com/productcategorizationnew1.jpg)

## Support for languages

Classification service supports classifications of websites in 30+ major languages, including English, French, German, Italian, Spanish, Chinese and others.  

## Offline database of categorized domains

We offer offline [URL database](https://www.websitecategorizationapi.com/url_database.php) of millions of categorized domains. It can be used web content filtering, AdTech marketing, cybersecurity, brand safety, contextual targeting. 

It is ideal for those use cases where you require very low latency of requests, which can be achieved with pre-classified websites stored in database. 

## Example classifications

Example classification for website www.github.com:
```
{
  "classification": [
    {
      "category": "Technology & Computing",
      "value": 0.7621352908406164
    },
    {
      "category": "Business and Finance",
      "value": 0.0785701408756428
    },
    {
      "category": "Video Gaming",
      "value": 0.06626958968249749
    },
    {
      "category": "Fine Art",
      "value": 0.017105357862223433
    },
    {
      "category": "Hobbies & Interests",
      "value": 0.016812511656388394
    },
    {
      "category": "Sports",
      "value": 0.011396157737341801
    },
    {
      "category": "Home & Garden",
      "value": 0.009099685741207822
    },
    {
      "category": "Personal Finance",
      "value": 0.0076400890345109055
    },
    {
      "category": "News and Politics",
      "value": 0.006692288300928684
    },
    {
      "category": "Careers",
      "value": 0.0039930258544077606
    },
    {
      "category": "Automotive",
      "value": 0.0029276292555247764
    },
    {
      "category": "Events and Attractions",
      "value": 0.0026449624402393084
    },
    {
      "category": "Shopping",
      "value": 0.0023606962223306537
    },
    {
      "category": "Family and Relationships",
      "value": 0.0023174171750800186
    },
    {
      "category": "Music and Audio",
      "value": 0.0020517145262615513
    },
    {
      "category": "Movies",
      "value": 0.0018936850100483473
    },
    {
      "category": "Travel",
      "value": 0.0009448942095545797
    },
    {
      "category": "Science",
      "value": 0.0008432696857311802
    },
    {
      "category": "Pets",
      "value": 0.0006956402098649299
    },
    {
      "category": "Television",
      "value": 0.0005261918310662409
    },
    {
      "category": "Real Estate",
      "value": 0.0005058920662560916
    },
    {
      "category": "Religion & Spirituality",
      "value": 0.000492253420442475
    },
    {
      "category": "Healthy Living",
      "value": 0.0004690261931844088
    },
    {
      "category": "Medical Health",
      "value": 0.0004467617749304944
    },
    {
      "category": "Education",
      "value": 0.00036333686743226124
    },
    {
      "category": "Food & Drink",
      "value": 0.0003463620639422737
    },
    {
      "category": "Books and Literature",
      "value": 0.00027078317064036986
    },
    {
      "category": "Style & Fashion",
      "value": 0.00011770141998920516
    },
    {
      "category": "Pop Culture",
      "value": 0.00006764487171529734
    }
  ],
  "html": "29101",
  "language": "en",
  "status": 200
}
```

## Useful resources used in development of website categorization

- [Tensorflow](https://www.tensorflow.org/)

- [Website categorization](https://medium.com/website-categorization/website-categorization-api-ca6c3e0f6c4d)

- [Sklearn](https://scikit-learn.org/stable/)

- [Introduction to URL Categorization Database](https://www.alpha-quantum.com/blog/url-database/url-database/) 

- [Top shopify stores](https://www.onlinestores.ai)



