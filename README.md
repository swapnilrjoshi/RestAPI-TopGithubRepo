# RestAPI-Getting Top 3 Repositories Of an Orgnization

Rest API to fetch top 3 repositories of an organization sorted by number of stars

## Usage

Successful response will have a following form
```json
{
	"results": [ 
		{"name": "name of the repository within an organization with higest stars", "stars": number of stars for that repository}
		{"name": "name of the repository with second higest number of stars", "stars": number of stars for that repository}
		{"name": "name of the repository with third higest number of stars", "stars": number of stars for that repository}
	]
}
```

If an organization have less than 3 repositories then the response will that many repositories sorted based on number of stars accordingly

Unsuccessful response will have the following form
```json
{
	"message": "Error message"
}
```


### Defination

'POST /repo'

### Response 
- 200 OK
- 429 TOO MANY REQUESTS

```json
{
	"org": "github-organization-name"
}
```
