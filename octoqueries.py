import GraphQLClient


def get_mpn_string(mpn_list):
    """
    This function is used to extract and format a string from the mpns extracted from the BOM file to be used for
    a query.
    """
    str_mpns: str = ""
    for mpn in mpn_list:
        str_mpns += '{mpn: \"%s\"}, ' % mpn

    return str_mpns


def mpn_query(client, mpn_list):
    """
    This function runs a query of manufacturer part numbers (mpns) against the OctoPart API. Since, OctoPart requires
    an OctoPart id to be able to look up price, stock, and lead time information, we have to first obtain the
    OctoPart id by running a query with the mpns. The API allows us to do this through a Multimatch query; multimatch
    is used to query multiple parts at once and allows the user to search for part information by mpn per the
    OctoPart API Documentation. The query returns a json object with the API data, which is returned by the function.
    """
    str_mpns = get_mpn_string(mpn_list)
    query = '''
            {
              multi_match(
                queries: [
                 %s
                ]
              ) {
                hits
                parts {
                  id
                  mpn
                  manufacturer {
                    name
                  }
                }
                error
              }
            }
    ''' % str_mpns
    resp = client.execute(query)

    return resp


def octoid_query(client, id_list):
    """
    This function is used to run the query of OctoPart ids against the API. The query returns a json object with
    each part's OctoPart id, manufacturer, seller authorization status, seller name, seller country, each seller's
    inventory level per listing, each seller's prices per listing, factory lead days per listing, and a description
    of each part.
    """
    query = '''
    query get_parts($ids: [String!]!) {
        parts(ids: $ids) {
            id
            manufacturer {
                name
            }
            mpn

            sellers {
                is_authorized
                company {
                    name
                    is_verified
                }
                country
                offers {
                    inventory_level
                    prices {
                        price
                    }
                    factory_lead_days
                }
            }

            short_description
        }
    }
    '''
    ids = [str(octoid) for octoid in id_list]
    resp = client.execute(query, {'ids': ids})

    return resp
