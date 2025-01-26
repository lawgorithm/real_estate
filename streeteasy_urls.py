import pandas as pd

ROOT_URL = 'https://streeteasy.com/for-sale/nyc'

TYPES = {
    'Multifamily': 'M',
    'Condo': 'D1',
    'Coop': 'P1',
    'House': 'X'
}

BEDS = {
    'Studio': 'beds:0',
    '1': 'beds:1',
    '1+': 'beds%3E=1',
    '2': 'beds:2',
    '2+': 'beds%3E=2',
    '3': 'beds:3',
    '3+': 'beds%3E=3',
    '4+': 'beds%3E=4',
}

BATHS = {
    '1+': '1',
    '1.5+': '1.5',
    '2+': '2',
    '3+': '3',
}

AREAS = {
    "Boerum Hill": 306,
    "Brooklyn": 300,
    "Brooklyn Heights": 305,
    "Carroll Gardens": 321,
    "Clinton Hill": 364,
    "Cobble Hill": 322,
    "Columbia St Waterfront District": 328,
    "Ditmas Park": 343,
    "Downtown Brooklyn": 303,
    "Fort Greene": 304,
    "Gowanus": 320,
    "Greenpoint": 301,
    "Greenwood": 367,
    "Park Slope": 319,
    "Prospect Heights": 326,
    "Prospect Park South": 355,
    "Red Hook": 318,
    "Sunset Park": 323,
    "Windsor Terrace": 324,
    "Williamsburg": 302,
}

FAV_NEIGHBORHOODS = [
    "Boerum Hill",
    "Brooklyn Heights",
    "Carroll Gardens",
    "Clinton Hill",
    "Cobble Hill",
    "Columbia St Waterfront District",
    "Ditmas Park",
    "Downtown Brooklyn",
    "Fort Greene",
    "Gowanus",
    "Greenpoint",
    "Greenwood",
    "Park Slope",
    "Prospect Heights",
    "Prospect Park South",
    "Red Hook",
    "Sunset Park",
    "Windsor Terrace",
    "Williamsburg",
]

class StreetEasyParams:
    """
    Class to represent StreetEasy search parameters.

    Attributes:
        apt_type: The type of apartment (e.g., "o-op", "Condo").
        min_price: The minimum price of the apartment.
        max_price: The maximum price of the apartment.
        area: The desired area or neighborhood.
        beds: The number of bedrooms.
        baths: The number of bathrooms.
        description: Optional keywords to search in the property description.
    """
    def __init__(
        self,
        apt_type=None,
        min_price=None,
        max_price=None,
        area=None,
        beds=None,
        baths=None,
        description=None,
    ):
      """
      Initializes a StreetEasyParams object with the given parameters.

      Args:
          apt_type: The type of apartment.
          min_price: The minimum price of the apartment.
          max_price: The maximum price of the apartment.
          area: The desired area or neighborhood.
          beds: The number of bedrooms.
          baths: The number of bathrooms.
          description: Optional keywords to search in the property description.
      """
      if apt_type:
        assert apt_type in TYPES.keys(), 'Invalid apt_type'
      if beds:
        assert beds in BEDS.keys(), 'Invalid beds'
      if baths:
        assert baths in BATHS.keys(), 'Invalid baths'
      self.apt_type = apt_type
      self.min_price = min_price
      self.max_price = max_price
      self.area = area
      self.beds = beds
      self.baths = baths
      self.description = description

def streeteasy_url_pars(
    apt_type=None, min_price=None, max_price=None, area=300,
    beds=None, baths=None, description=None):
  """
  Generates StreetEasy URL parameters based on given criteria.

  Args:
      apt_type: The type of apartment (e.g., "studio", "1-bedroom").
      min_price: The minimum price of the apartment.
      max_price: The maximum price of the apartment.
      area: The desired area or neighborhood (can be a string or an integer ID).
      beds: The number of bedrooms.
      baths: The number of bathrooms.
      description: Optional keywords to search in the property description.

  Returns:
      A string of URL parameters for StreetEasy search.
  """
  if apt_type:
    apt_type = TYPES[apt_type]
    apt_type = f'type:{apt_type}%7C'
  prices = ['', '']
  if min_price:
    prices[0] = str(min_price)
  if max_price:
    prices[1] = str(max_price)
  if prices == ['', '']:
    prices = None
  else:
    prices = '-'.join(prices)
    prices = f'price:{prices}'
  if area:
    x = [str(AREAS[x]) for x in area]
    x = ','.join(x)
    area = f'area:{x}'
  if beds:
    beds = BEDS[beds]
  if baths:
    baths = str(BATHS[baths])
    baths = f'baths%3E={baths}'
  if description:
    description = description.replace('"', '%22').replace(' ', '%20')
    description = f'description:{description}'
  par_list = [apt_type, prices, area, beds, baths, description]
  par_list = [x for x in par_list if x]
  url_pars = '|'.join(par_list)
  return url_pars

def streeteasy_url(pars):
  """
  Generates a full StreetEasy URL based on given StreetEasyParams object.

  Args:
      pars: A StreetEasyParams object containing search parameters.

  Returns:
      A string representing the full StreetEasy URL.

  Raises:
      AssertionError: If the provided 'pars' is not an instance of StreetEasyParams.
  """
  assert isinstance(pars, StreetEasyParams), 'pars must be StreetEasyParams obj'
  url_pars = streeteasy_url_pars(
      apt_type=pars.apt_type,
      min_price=pars.min_price,
      max_price=pars.max_price,
      area=pars.area,
      beds=pars.beds,
      baths=pars.baths,
      description=pars.description)
  url = f'{ROOT_URL}/{url_pars}'
  return url

descriptions = []
urls = []

desc1 = '3+ Bedroom homes in Carroll Gardens'
url1 = streeteasy_url(
    pars=StreetEasyParams(
        max_price=4000000,
        area=['Carroll Gardens'],
        beds='3+',
        )
    )

desc2 = '3+ Bedroom homes in favorite BK neighborhoods in lower price range'
url2 = streeteasy_url(
    pars=StreetEasyParams(
        min_price=800000,
        max_price=1500000,
        area=FAV_NEIGHBORHOODS,
        beds='3+',
        )
    )
desc3 = '3+ Bedroom homes in favorite BK neighborhoods with duplex'
url3 = streeteasy_url(
    pars=StreetEasyParams(
        max_price=4000000,
        area=FAV_NEIGHBORHOODS,
        beds='3+',
        description='duplex',
        )
    )
desc4 = '3+ Bedroom homes in favorite BK neighborhoods with triplex'
url4 = streeteasy_url(
    pars=StreetEasyParams(
        max_price=4000000,
        area=FAV_NEIGHBORHOODS,
        beds='3+',
        description='triplex',
        )
    )
desc5 = '3+ Bedroom homes in Ditmas Park'
url5 = streeteasy_url(
    pars=StreetEasyParams(
        area=['Ditmas Park'],
        beds='3+',
        )
    )
desc6 = 'Apartments in Museum Court'
url6 = streeteasy_url(
    pars=StreetEasyParams(
        description='"Museum Court"',
        )
    )
desc7 = 'Apartments in Turner Towers'
url7 = streeteasy_url(
    pars=StreetEasyParams(
        description='"Turner Towers"',
        )
    )
desc8 = 'Apartments in The Abraham Lincoln'
url8 = streeteasy_url(
    pars=StreetEasyParams(
        description='"Abraham Lincoln"',
        )
    )
desc9 = 'Apartments in Ansonia Court (watch factory)'
url9 = streeteasy_url(
    pars=StreetEasyParams(
        description='Ansonia',
        )
    )

desc10 = 'Apartments in The Traymore'
url10 = streeteasy_url(
    pars=StreetEasyParams(
        description='"The Traymore"',
        )
    )

descriptions.append(desc1)
descriptions.append(desc2)
descriptions.append(desc3)
descriptions.append(desc4)
descriptions.append(desc5)
descriptions.append(desc6)
descriptions.append(desc7)
descriptions.append(desc8)
descriptions.append(desc9)
descriptions.append(desc10)

urls.append(url1)
urls.append(url2)
urls.append(url3)
urls.append(url4)
urls.append(url5)
urls.append(url6)
urls.append(url7)
urls.append(url8)
urls.append(url9)
urls.append(url10)

print(desc1)
print(url1)
print()
print(desc2)
print(url2)
print()
print(desc3)
print(url3)
print()
print(desc4)
print(url4)
print()
print(desc5)
print(url5)
print()
print(desc6)
print(url6)
print()
print(desc7)
print(url7)
print()
print(desc8)
print(url8)
print()
print(desc9)
print(url9)
print()
print(desc10)
print(url10)
print()

df = pd.DataFrame({
    'descriptions': descriptions,
    'urls': urls,
})
df.to_csv('testy_mctest_streeteasy.csv', index=False)
