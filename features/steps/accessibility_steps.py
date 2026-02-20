from behave import then


@then('every image on the page should have alt text')
def step_verify_all_images_have_alt(context):
    result = context.page.evaluate("""
        () => {
            const images = Array.from(document.images);
            const missing = images.filter(img => !img.alt || img.alt.trim() === '');
            return {
                total: images.length,
                missing: missing.map(img => img.src)
            };
        }
    """)
    assert len(result["missing"]) == 0, (
        f"{len(result['missing'])} of {result['total']} images missing alt text: {result['missing']}"
    )


@then('there should be exactly {count:d} h1 element')
def step_verify_h1_count(context, count):
    h1_count = context.page.locator('h1').count()
    assert h1_count == count, f"Expected {count} h1 element(s), found {h1_count}"


@then('headings should follow a logical order')
def step_verify_heading_order(context):
    levels = context.page.evaluate("""
        () => Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'))
              .map(h => parseInt(h.tagName[1]))
    """)
    for i in range(1, len(levels)):
        gap = levels[i] - levels[i - 1]
        assert gap <= 1, (
            f"Heading level jumps from h{levels[i-1]} to h{levels[i]} at position {i} — "
            f"headings should not skip levels"
        )


@then('the html element should have a lang attribute')
def step_verify_lang_attribute(context):
    lang = context.page.evaluate("() => document.documentElement.lang")
    assert lang and len(lang) > 0, "HTML element is missing the lang attribute"


@then('all links should have non-empty href attributes')
def step_verify_links_have_href(context):
    result = context.page.evaluate("""
        () => {
            const links = Array.from(document.querySelectorAll('a'));
            const bad = links.filter(a => !a.href || a.href === '' || a.href === '#');
            return {
                total: links.length,
                bad: bad.map(a => ({text: a.textContent.trim(), href: a.href}))
            };
        }
    """)
    assert len(result["bad"]) == 0, (
        f"{len(result['bad'])} links have empty hrefs: {result['bad']}"
    )


@then('the submit button should be focusable')
def step_verify_submit_focusable(context):
    is_focusable = context.page.evaluate("""
        () => {
            const btn = document.querySelector('input[type="submit"], button[type="submit"]');
            if (!btn) return false;
            return btn.tabIndex >= 0;
        }
    """)
    assert is_focusable, "Submit button is not keyboard focusable"


@then('the body text should have a minimum font size of {min_px:d}px')
def step_verify_min_font_size(context, min_px):
    result = context.page.evaluate("""
        (minPx) => {
            const elements = document.querySelectorAll('p, li, td, span, a, label');
            const tooSmall = [];
            for (const el of elements) {
                const size = parseFloat(getComputedStyle(el).fontSize);
                if (size < minPx && el.offsetWidth > 0 && el.offsetHeight > 0) {
                    tooSmall.push({tag: el.tagName, text: el.textContent.trim().substring(0, 30), size});
                }
            }
            return {total: elements.length, tooSmall};
        }
    """, min_px)
    assert len(result["tooSmall"]) == 0, (
        f"{len(result['tooSmall'])} elements below {min_px}px: {result['tooSmall'][:5]}"
    )
