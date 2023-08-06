## panther-okta
Panther Config SDK repo for Okta content


### Install all content with defaults:
```python
import panther_okta as okta

okta.use_all_with_defaults()
```


### Install a single rule with overrides:
```python
from panther_config import detection
from panther_utils import match_filters
import panther_okta as okta

okta.rules.account_support_access(
    # optionally, provide overrides
    overrides=detection.RuleOptions(
        # override the default "reference"
        reference="https://security-wiki.megacorp.internal/okta-incident-response",
    ),
    # optionally, provide pre-filters to be added to the defaults
    pre_filters=[
        match_filters.deep_equal("version", "0"),
    ]
)
```