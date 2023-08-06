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
import panther_okta as okta

okta.rules.account_support_access(
    overrides=detection.RuleOptions(
        # override the default "reference"
        reference="https://security-wiki.megacorp.internal/okta-incident-response",
    )
)
```