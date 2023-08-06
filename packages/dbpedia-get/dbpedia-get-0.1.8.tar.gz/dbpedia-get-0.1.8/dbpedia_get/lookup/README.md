# dbpedia lookup
Access dbPedia pages over-the-wire live from dbpedia's main site

This guarantees fresh content and gives us more control over the content and format

However, it is a good deal slower than using a local version of Wikipedia.

## Usage:
```powershell
.\resources\scripts\Run-Dbpedia-Lookup.ps1 -EntityType "architecture" -EntityName "network_architecture" -EntityLabel "Network Architecture"
```

If this entity exists in dbPedia it will be retrieved as a JSON page.  If this entity exists in the local cache, it will be retrieved from the cache as a JSON page.

## JSON
This is an abbreviated sample of the JSON page
```json
{
    "key": "network_architecture",
    "url": "https://en.wikipedia.org/wiki/Network_architecture",
    "title": "Network architecture",
    "links": [
        "ACM Computing Classification System",
        "ASCII",
        "ASN.1",
        "Abstraction layer",
        "Address Resolution Protocol",
        "Algorithm",
        "Algorithm design",        
    ],
    "content": [
        "Network architecture is the design of a computer network.",
        "It framework for the specification of a network's physical components and their functional organization and configuration, its operational principles and procedures, as well as communication protocols used.",
        "In telecommunication, the specification of a network architecture may also include a detailed description of products and services delivered via a communications network, as well as detailed rate and billing structures under which services are compensated.",
        "The network architecture of the Internet is predominantly expressed by its use of the Internet protocol suite, rather than a specific model for interconnecting networks or nodes in the network, or the usage of specific types of hardware links.",
        "== OSI model ==.",
    ],
    "page_id": "41406",
    "summary": [
        "Network architecture is the design of a computer network.",
        "It framework for the specification of a network's physical components and their functional organization and configuration, its operational principles and procedures, as well as communication protocols used.",
        "In telecommunication, the specification of a network architecture may also include a detailed description of products and services delivered via a communications network, as well as detailed rate and billing structures under which services are compensated.",
        "The network architecture of the Internet is predominantly expressed by its use of the Internet protocol suite, rather than a specific model for interconnecting networks or nodes in the network, or the usage of specific types of hardware links."
    ],
    "sections": [],
    "parent_id": "1094813181",
    "categories": [
        "Network architecture",
        "Telecommunications engineering",
    ],
    "references": [
        "http://www.its.bldrdoc.gov/fs-1037/fs-1037c.htm",
        "http://www.bls.gov/ooh/computer-and-information-technology/computer-network-architects.htm",
    ],
    "revision_id": "1095285384",
    "original_title": "Network architecture",
    "entity": {
        "type": "architecture",
        "name": "network_architecture",
        "label": "Network Architecture"
    }
}
```