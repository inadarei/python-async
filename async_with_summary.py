import aiohttp
import asyncio
import json
import uvloop # optional. @see https://github.com/MagicStack/uvloop

base_url = "https://www.googleapis.com/books/v1/volumes?q="

async def fetch(url):
  '''
  fetches contents of a URL asynchronously
  '''
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      return await response.text()

async def book_authors(isbn):
  '''
  returns all authors of a book
  '''
  book_url = f"{base_url}isbn:{isbn}" # "Microservice Architecture"
  book_info = await fetch(book_url)
  json_response = json.loads(book_info)
  authors = json_response['items'][0]['volumeInfo']['authors']
  return authors

async def authorNumBooks(author_name):
  '''
  returns number of books published by an author
  '''
  author_url = f"{base_url}inauthor:{author_name}"
  print(f"Quering: {author_name}")
  author_info = await fetch(author_url)
  print(f"Fetched: {author_name}")
  author_info_json = json.loads(author_info)
  count = author_info_json['totalItems']
  return {"name" : author_name, "count": count}

async def msa_authors():
  authors = await book_authors(1491956224) # "Microservice Architecture"
  futures = [authorNumBooks(author) for author in authors]

  resolved_infos = await asyncio.gather(*futures)
  return resolved_infos

async def main():
    author_stat_results = await msa_authors()
    print("==== Author stats results: ====")
    pp = [f"  {item['name']} : {item['count']}" for item in author_stat_results]
    print('\n'.join(pp))

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy()) # optional: higher performance
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# @see: https://github.com/timofurrer/awesome-asyncio    