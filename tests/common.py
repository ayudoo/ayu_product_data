from odoo.tests.common import SavepointCase


class ProductDataTestCommon(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Attribute

        cls.prod_att_1 = cls.env["product.attribute"].create({"name": "Size"})
        cls.prod_attr1_v1 = cls.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": cls.prod_att_1.id, "sequence": 1}
        )
        cls.prod_attr1_v2 = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.prod_att_1.id, "sequence": 2}
        )
        cls.prod_attr1_v3 = cls.env["product.attribute.value"].create(
            {"name": "L", "attribute_id": cls.prod_att_1.id, "sequence": 3}
        )

        # Tags

        cls.tag_category_color = cls.env.ref("ayu_product_data.tag_category_color")
        cls.tag_category_material = cls.env.ref(
            "ayu_product_data.tag_category_material"
        )
        cls.tag_category_detail = cls.env.ref("ayu_product_data.tag_category_detail")

        Tag = cls.env["ayu_product_data.tag"]

        cls.tag_detail1 = Tag.create(
            {
                "category_id": cls.tag_category_detail.id,
                "name": "Product Detail1",
            }
        )
        cls.tag_detail2 = Tag.create(
            {
                "category_id": cls.tag_category_detail.id,
                "name": "Product Detail2",
            }
        )
        cls.tag_detail3 = Tag.create(
            {
                "category_id": cls.tag_category_detail.id,
                "name": "Product Detail3",
            }
        )
        cls.tag_detail4 = Tag.create(
            {
                "category_id": cls.tag_category_detail.id,
                "name": "Product Detail4",
            }
        )

        cls.tag_white = Tag.create(
            {
                "category_id": cls.tag_category_color.id,
                "name": "Shades of White",
            }
        )
        cls.tag_black = Tag.create(
            {
                "category_id": cls.tag_category_color.id,
                "name": "Shades of Black",
            }
        )

        cls.tag_material_cotton = Tag.create(
            {
                "category_id": cls.tag_category_material.id,
                "name": "Cotton",
            }
        )

        cls.tag_material_test1 = Tag.create(
            {
                "category_id": cls.tag_category_material.id,
                "name": "Material Test1",
            }
        )

        # Predefined data

        cls.age_group_adult = cls.env.ref("ayu_product_data.age_group_adult")
        cls.condition_new = cls.env.ref("ayu_product_data.condition_new")
        cls.gender_female = cls.env.ref("ayu_product_data.gender_female")
        cls.product_text_category_description = cls.env.ref(
            "ayu_product_data.product_text_category_description"
        )

        # Customer data

        cls.google_category = cls.env["ayu_product_data.google_category"].search(
            [], limit=1
        )

        PublicCategory = cls.env["product.public.category"]

        cls.public_category = PublicCategory.create(
            {
                "name": "Custom Product Type",
            }
        )

        Line = cls.env["ayu_product_data.line"]

        cls.line_a_series = Line.create(
            {
                "name": "A-Series",
            }
        )

        Color = cls.env["ayu_product_data.color"]

        cls.color_white = Color.create(
            {
                "identifier": "FFF",
                "name": "white",
            }
        )
        cls.color_black = Color.create(
            {
                "identifier": "000",
                "name": "black",
            }
        )

        Detail = cls.env["ayu_product_data.product_detail"]

        cls.detail_100_cotton = Detail.browse(
            Detail.name_create("Material Composition:100% Cotton")[0]
        )
        cls.detail_ecologic = Detail.browse(
            Detail.name_create("Sustainability:Ecologic")[0]
        )
        cls.detail_test2 = Detail.browse(Detail.name_create("Usage:Test2")[0])
        cls.detail_test3 = Detail.browse(Detail.name_create("Usage:Test3")[0])

        Highlight = cls.env["ayu_product_data.product_highlight"]

        cls.product_highlight = Highlight.create(
            {
                "name": "The highlight description",
            }
        )

        Material = cls.env["ayu_product_data.material"]

        cls.material_cotton = Material.create(
            {"name": "Cotton", "detail_ids": [cls.detail_100_cotton.id]}
        )
        cls.material_test1 = Material.create(
            {
                "name": "Test1",
            }
        )

        ItemGroup = cls.env["ayu_product_data.item_group"]

        cls.item_group_default = ItemGroup.create(
            {
                "identifier": "1",
                "name": "default",
                "ayu_color_id": cls.color_white.id,
                "custom_detail_ids": cls.detail_100_cotton.ids,
            }
        )

        cls.pt_wo_item_group = cls.env["product.template"].create(
            {
                "name": "Unique",
            }
        )

        cls.pt_item_group = cls.env["product.template"].create(
            {
                "name": "White Group",
                "ayu_item_group_id": cls.item_group_default.id,
            }
        )
