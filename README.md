# oblio_api_python
 Oblio.eu API implementation for Python

## create invoice
```
from oblio_api import OblioApi, OblioException

data = {
    'cif'                : '',
    'client'             : {
        'cif'           : '',
        'name'          : '',
        'rc'            : '',
        'code'          : '',
        'address'       : '',
        'state'         : '',
        'city'          : '',
        'country'       : '',
        'iban'          : '',
        'bank'          : '',
        'email'         : '',
        'phone'         : '',
        'contact'       : '',
        'vatPayer'      : '',
    },
    'dueDate'            : '',
    'deliveryDate'       : '',
    'collectDate'        : '',
    'seriesName'         : 'FCT',
    'collect'            : {},
    'referenceDocument'  : {},
    'language'           : 'RO',
    'precision'          : 2,
    'currency'           : 'RON',
    'products'           : [
        {
            'name'          : 'Abonament',
            'code'          : '',
            'description'   : '',
            'price'         : '100',
            'measuringUnit' : 'buc',
            'currency'      : 'RON',
            'vatName'       : 'Normala',
            'vatPercentage' : 19,
            'vatIncluded'   : True,
            'quantity'      : 2,
            'productType'   : 'Serviciu',
        }
    ],
    'issuerName'         : '',
    'issuerId'           : '',
    'noticeNumber'       : '',
    'internalNote'       : '',
    'deputyName'         : '',
    'deputyIdentityCard' : '',
    'deputyAuto'         : '',
    'selesAgent'         : '',
    'mentions'           : 'Factura facuta din python',
    'value'              : 0,
    'workStation'        : 'Sediu',
    'useStock'           : 0,
}

if __name__ == '__main__':
    try:
        email = ''
        secret = ''
        api = OblioApi(email, secret)

        response = api.create_doc('invoice', data)
        print(response)

    except OblioException as e:
        print(e.text)
```