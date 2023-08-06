from unittest import TestCase

from notionizer import Notion
from notionizer import Property as Prop
from notionizer import NumberFormat as NumForm
from notionizer import OptionColor as OptColor
from notionizer import RollupFunction as RFunc


class TestPage(TestCase):
    def test_get_properties(self):
        self.fail()


class TestPage(TestCase):

    # TODO: build up fully test
    def dtest_create_database(self):
        notion = Notion('secret_rvDkx9qH8AVG3aKBVwZ4r5Byo75uoAPMrQ1I6bo4d6G')
        page = notion.get_page('e8d28d7c0056414582fe23f2ab7c3928')
        db = page.create_database(
            title='test1',
            # emoji="🎉",
            # cover='https://media.wired.com/photos/5b899992404e112d2df1e94e/master/pass/trash2-01.jpg',
            properties=[
                Prop.RichText("text filed"),
                Prop.Number("number", format=NumForm.dollar),
                Prop.Select("select", options={'opt1': OptColor.blue, 'opt2': OptColor.red}),
                Prop.MultiSelect("multi select", options={'opt1': OptColor.blue, 'opt2': OptColor.red}),
                Prop.Relation("relation", "44d6b8fda2734f04968a771a79f97fb6"),
                Prop.Rollup(
                    "rollup",
                    rollup_property_name="Title",
                    relation_property_name="relation",
                    function=RFunc.count,
                ),
            ]
        )
        # print(page.get_properties())
    def test_option(self):
        notion = Notion('secret_rvDkx9qH8AVG3aKBVwZ4r5Byo75uoAPMrQ1I6bo4d6G')
        db = notion.get_database('44d6b8fda2734f04968a771a79f97fb6')
        prop_select = db.properties['Select']
        print(dir(prop_select))


