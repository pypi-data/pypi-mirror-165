from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'Dilbilimcilerin ihtiyaçları doğrultusunda geliştirilen concordance aracı'
LONG_DESCRIPTION = 'Concordance aranan sözcüğün önündeki ve arkasındaki dört sözcüğe bakıp excel dosyasına aktaran ' \
                   'fonksiyon '

# Setting up
setup(
    name="concordance",
    version=VERSION,
    author="İlker Atagün",
    author_email="<ilker.atagun@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'nltk==3.5', 'regex==2020.11.13', "click==7.1.2", "joblib==1.0.1", "tqdm==4.59.0"],
    keywords=['python', 'nlp', 'linguistics', 'concordance'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
