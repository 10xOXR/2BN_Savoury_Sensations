import math


class Helpers:

    @staticmethod
    def dropdowns(coll1, coll2, coll3):
        return (([
            item for cuisine in coll1.find()
            for item in cuisine.get("cuisineType")]),
            ([
                item for course in coll2.find()
                for item in course.get("courseType")]),
            ([
                item for allergen in coll3.find()
                for item in allergen.get("allergenType")]))


    @staticmethod
    def pagination(recipe_args, page_args, collection):
        page_count = (
        range(1, (math.ceil(recipe_args.count() / 8)) + 1)
        if recipe_args.count() != 0 else "")
        count = (
        page_args * 8 if (page_args * 8) < recipe_args.count()
        else recipe_args.count())
        pages = [page for page in page_count] if page_count != "" else []
        previous_page = page_args - 1 if page_args != 1 else 1
        if page_count == "" or pages == []:
            next_page = ""
        else:
            next_page = page_args + 1 if page_args < pages[-1] else page_args
        total_recipes = collection.count()
        results_count = recipe_args.count()
        return (
            pages, previous_page, next_page, count,
            total_recipes, results_count)