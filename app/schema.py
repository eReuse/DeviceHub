"""
We mimic https://schema.org/unitCode, in concrete
the UN/CEFACT Common Code.
"""
import copy


class UnitCodes:
    mbyte = '4L'
    mbps = 'E20'
    mhz = 'MHZ'
    gbyte = 'E34'
    ghz = 'A86'
    bit = 'A99'
    kgm = 'KGM'
    m = 'MTR'


rdfs = {
    'label': {
        'type': 'string',
        'sink': 5,
        'description': 'A short, descriptive title'
    },
    '@type': {
        'type': 'string',
        'required': True,
        'allowed': []
    }
}

thing = dict(rdfs, **{
    'url': {
        'type': 'url',
        'readonly': True
    },
    'sameAs': {
        'type': 'url'
    },
    'description': {
        'type': 'string',
        'maxlength': 500,
        'sink': -4,
        'description': 'Full long description'
    }
})
