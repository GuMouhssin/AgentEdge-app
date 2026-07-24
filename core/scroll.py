


def load_more_results(page, target_count):
    scrollable = page.locator('div[role="feed"]')

    prev_count = 0
    no_progress = 0
    MAX_NO_PROGRESS = 3

    while True:

        curr_count = page.locator("a.hfpxzc").count()

        if curr_count >= target_count:
            return

        if curr_count > prev_count:
            prev_count = curr_count
            no_progress = 0

        else:
            no_progress += 1

            if no_progress >= MAX_NO_PROGRESS:
                return

        scrollable.evaluate(
            "(el) => el.scrollBy(0, el.scrollHeight)"
        )

        page.wait_for_load_state("networkidle")
