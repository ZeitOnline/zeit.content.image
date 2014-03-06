# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from zeit.cms.checkout.helper import checked_out
from zeit.cms.content.reference import ReferenceProperty
from zeit.cms.interfaces import ICMSContent
from zeit.cms.testcontenttype.testcontenttype import TestContentType
from zeit.content.image.interfaces import IImageMetadata
import zeit.cms.testing
import zeit.content.image.interfaces
import zeit.content.image.testing


class ImageAssetTest(zeit.cms.testing.FunctionalTestCase):

    layer = zeit.content.image.testing.ZCML_LAYER

    def test_IImages_accepts_IImage_for_backwards_compatibility(self):
        with self.assertNothingRaised():
            zeit.content.image.interfaces.IImages['image'].validate(
                ICMSContent('http://xml.zeit.de/2006/DSC00109_2.JPG'))


class ImageReferenceTest(zeit.cms.testing.FunctionalTestCase):

    layer = zeit.content.image.testing.ZCML_LAYER

    def setUp(self):
        super(ImageReferenceTest, self).setUp()
        TestContentType.images = ReferenceProperty('.body.image', 'image')

    def tearDown(self):
        del TestContentType.images
        super(ImageReferenceTest, self).tearDown()

    def test_local_values_override_original_ones(self):
        image = ICMSContent('http://xml.zeit.de/2006/DSC00109_2.JPG')
        content = self.repository['testcontent']
        ref = content.images.create(image)
        content.images = (ref,)
        ref.title = u'locally'
        self.assertEqual('locally', ref.xml.get('title'))

        ref.update_metadata()
        self.assertEqual('locally', ref.xml.get('title'))

    def test_empty_local_values_leave_original_ones_alone(self):
        image = ICMSContent('http://xml.zeit.de/2006/DSC00109_2.JPG')
        with checked_out(image) as co:
            IImageMetadata(co).title = 'originally'
        content = self.repository['testcontent']
        ref = content.images.create(image)
        content.images = (ref,)
        self.assertEqual('originally', ref.xml.get('title'))
        ref.update_metadata()
        self.assertEqual('originally', ref.xml.get('title'))