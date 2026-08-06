"""Local compatibility surface for Kessoku's native primary navigation.

The application previously imported the third-party ``streamlit-option-menu``
package. Keeping this tiny compatibility module lets the route layer remain
stable while the rendered control is now owned by ``kessoku_site.navigation``.
"""

from kessoku_site.navigation import option_menu

__all__ = ["option_menu"]
