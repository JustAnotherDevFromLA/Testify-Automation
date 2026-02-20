import time

from behave import then, when


@when('the user measures the page load time')
def step_measure_load_time(context):
    start = time.time()
    context.home_page.navigate_home()
    end = time.time()
    context.load_time = end - start


@then('the page should load in less than {max_seconds:d} seconds')
def step_verify_load_time(context, max_seconds):
    assert context.load_time < max_seconds, (
        f"Page took {context.load_time:.1f}s to load, expected < {max_seconds}s"
    )


@then('all images should load successfully')
def step_verify_no_broken_images(context):
    result = context.page.evaluate("""
        () => {
            const images = Array.from(document.images);
            const broken = images.filter(img => !img.complete || img.naturalWidth === 0);
            return {
                total: images.length,
                broken: broken.map(img => img.src)
            };
        }
    """)
    assert len(result["broken"]) == 0, (
        f"{len(result['broken'])} of {result['total']} images failed to load: {result['broken']}"
    )


@then('the total DOM element count should be less than {max_count:d}')
def step_verify_dom_size(context, max_count):
    count = context.page.evaluate("() => document.getElementsByTagName('*').length")
    assert count < max_count, f"DOM has {count} elements, expected < {max_count}"
