from odoo.tests.common import TransactionCase
from . import common


class TestTagsCategory(TransactionCase):
    def test_get_tag_category(self):
        for model_name in [
            "line",
            "age_group",
            "color",
            "condition",
            "gender",
            "material",
        ]:
            Model = self.env["ayu_product_data.{}".format(model_name)]
            tag_category = self.env.ref(
                "ayu_product_data.tag_category_{}".format(model_name)
            )
            self.assertEqual(Model._get_tag_category(), tag_category)


class TestTags(common.ProductDataTestCommon):
    def test_assign_color_tag(self):
        template = self.pt_wo_item_group
        color = self.color_black
        template.ayu_color_id = color.id

        self.assertFalse(template.ayu_tag_rel_ids)

        # add tags to color, updates template
        color.tag_ids = [self.tag_white.id, self.tag_black.id]
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [self.tag_white.id, self.tag_black.id]
        )

        color.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_color.id,
                    "name": "Shades of Gray",
                },
            )
        ]
        template.invalidate_cache()

        self.assertEqual(template.ayu_tag_rel_ids.tag_id, color.tag_ids)

        # add tags to color, updates template
        color.tag_ids = [self.tag_black.id]
        template.invalidate_cache()

        self.assertEqual(template.ayu_tag_rel_ids.tag_id.ids, [self.tag_black.id])

    def test_item_group_color_tag(self):
        template = self.pt_item_group
        color = template.ayu_item_group_id.ayu_color_id

        self.assertFalse(template.ayu_tag_rel_ids)

        color.tag_ids = [self.tag_white.id, self.tag_black.id]
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [self.tag_white.id, self.tag_black.id]
        )

    def test_assign_detail_tag(self):
        template = self.pt_wo_item_group
        detail = self.detail_ecologic
        template.ayu_custom_product_detail_ids = [detail.id]

        self.assertFalse(template.ayu_tag_rel_ids)

        detail.tag_ids = [self.tag_detail1.id, self.tag_detail2.id]
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [
                self.tag_detail1.id, self.tag_detail2.id]
        )

        detail.tag_ids = [self.tag_detail2.id]
        template.invalidate_cache()

        self.assertEqual(template.ayu_tag_rel_ids.tag_id.ids, [self.tag_detail2.id])

    def test_item_group_detail_tag(self):
        template = self.pt_item_group
        detail = template.ayu_item_group_id.detail_ids[0]

        self.assertFalse(template.ayu_tag_rel_ids)

        detail.tag_ids = [self.tag_detail2.id]
        template.invalidate_cache()
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id.ids,
                              [self.tag_detail2.id])

    def test_material_detail_tag(self):
        template = self.pt_item_group
        self.pt_item_group.ayu_material_id = self.material_cotton.id
        self.assertEqual(template.ayu_material_id, self.material_cotton)

        detail = self.material_cotton.detail_ids[0]
        detail.tag_ids = [self.tag_detail2.id]

        template.invalidate_cache()
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id.ids,
                              [self.tag_detail2.id])

    def test_assign_material_and_different_color(self):
        template = self.pt_wo_item_group
        color = self.color_black

        self.material_cotton.tag_ids = [self.tag_material_cotton.id]
        template.ayu_material_id = self.material_cotton.id

        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id.ids,
                              [self.tag_material_cotton.id])

        template.ayu_color_id = color.id
        color.tag_ids = [self.tag_black.id]

        self.color_white.tag_ids = [self.tag_white.id]
        template.invalidate_cache()

        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [
                self.tag_material_cotton.id, self.tag_black.id]
        )

        template.ayu_color_id = self.color_white
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [
                self.tag_material_cotton.id, self.tag_white.id]
        )

    def test_assign_detail_to_pt_material_and_ig(self):
        template = self.pt_item_group

        detail1 = self.detail_ecologic
        detail1.tag_ids = [self.tag_detail1.id]
        detail2 = self.detail_test2
        detail2.tag_ids = [self.tag_detail2.id]
        detail3 = self.detail_test3
        detail3.tag_ids = [self.tag_detail3.id]

        self.assertFalse(template.ayu_tag_rel_ids)

        # Test to replace detail 2 and 3 by 1 and 2
        template.ayu_custom_product_detail_ids = [detail2.id, detail3.id]
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [
                self.tag_detail2.id, self.tag_detail3.id]
        )

        template.ayu_custom_product_detail_ids = [detail1.id, detail2.id]
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [
                self.tag_detail1.id, self.tag_detail2.id]
        )

        # Test to replace Material with another one with 3 details
        template.ayu_custom_product_detail_ids = False
        template.ayu_material_id = self.material_test1.id
        template.ayu_material_id.tag_ids = [self.tag_material_test1.id]
        template.invalidate_cache()
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id.ids,
                              [self.tag_material_test1.id])

        new_material = self.env["ayu_product_data.material"].create(
            {
                "name": "new",
                "detail_ids": [detail1.id, detail2.id, detail3.id],
            }
        )
        template.ayu_material_id = new_material
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids,
            [self.tag_detail1.id, self.tag_detail2.id, self.tag_detail3.id],
        )

        # clear matieral on product template level
        template.ayu_material_id = False
        template.invalidate_cache()
        self.assertFalse(template.ayu_tag_rel_ids)

        # Test to add tags to detail item group
        detail_ig = template.ayu_item_group_id.detail_ids
        detail_ig.tag_ids = [self.tag_detail4.id]
        template.ayu_custom_product_detail_ids = False
        template.invalidate_cache()
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id.ids,
                              [self.tag_detail4.id])

        # Test to replace material of the item group
        item_group = template.ayu_item_group_id
        item_group.ayu_material_id = new_material
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids,
            [
                self.tag_detail1.id,
                self.tag_detail2.id,
                self.tag_detail3.id,
                self.tag_detail4.id,
            ],
        )

        # Test custom details on item group
        item_group.ayu_material_id = False
        template.ayu_material_id = False
        template.invalidate_cache()
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id.ids,
                              [self.tag_detail4.id])

        item_group.custom_detail_ids = [detail1.id, detail2.id]
        template.invalidate_cache()
        self.assertCountEqual(
            template.ayu_tag_rel_ids.tag_id.ids, [
                self.tag_detail1.id, self.tag_detail2.id]
        )

    def test_assign_age_group_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.age_group_adult
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": data_record._get_tag_category().id,
                    "name": "Adult Products",
                },
            )
        ]
        template.ayu_age_group_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_condition_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.condition_new
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": data_record._get_tag_category().id,
                    "name": "Totally New!",
                },
            )
        ]
        template.ayu_condition_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_gender_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.gender_female
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": data_record._get_tag_category().id,
                    "name": "Womenswear",
                },
            )
        ]
        template.ayu_gender_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_line_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.line_a_series
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": data_record._get_tag_category().id,
                    "name": "Our A-Series",
                },
            )
        ]
        template.ayu_line_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_public_category_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.public_category
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_detail.id,
                    "name": "Product Type Detail",
                },
            )
        ]
        template.public_categ_ids = [data_record.id]
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_google_category_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.google_category
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_detail.id,
                    "name": "Category Detail",
                },
            )
        ]
        template.ayu_google_category_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_item_group_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.item_group_default
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_detail.id,
                    "name": "Item Group Detail",
                },
            )
        ]
        template.ayu_item_group_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_product_description_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.env["ayu_product_data.product_text"].create(
            {
                "category_id": self.product_text_category_description.id,
                "identifier": "1",
                "content": "Default Description",
            }
        )
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_detail.id,
                    "name": "Description Tag",
                },
            )
        ]
        template.ayu_description_id = data_record
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_product_text_with_tags(self):
        template = self.pt_wo_item_group

        text_category = self.env["ayu_product_data.product_text_category"].create(
            {"name": "Other Category"}
        )
        data_record = self.env["ayu_product_data.product_text"].create(
            {
                "category_id": text_category.id,
                "identifier": "1",
                "content": "Default Description",
            }
        )
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_detail.id,
                    "name": "Product Text Tag",
                },
            )
        ]
        template.ayu_product_text_ids = [data_record.id]
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)

    def test_assign_product_highlight_with_tags(self):
        template = self.pt_wo_item_group
        data_record = self.product_highlight
        data_record.tag_ids = [
            (
                0,
                0,
                {
                    "category_id": self.tag_category_detail.id,
                    "name": "Highlight Tag",
                },
            )
        ]
        template.ayu_product_highlight_ids = data_record.ids
        self.assertCountEqual(template.ayu_tag_rel_ids.tag_id, data_record.tag_ids)
