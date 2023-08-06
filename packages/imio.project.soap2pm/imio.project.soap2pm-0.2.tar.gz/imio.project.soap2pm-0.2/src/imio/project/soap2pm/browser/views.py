## -*- coding: utf-8 -*-

from collective.task.interfaces import ITaskMethods
from Products.Five import BrowserView
from Products.CMFPlone.utils import safe_unicode


def object_link(obj, view='', title=''):
    href = view and "%s/%s" % (obj.absolute_url(), view) or obj.absolute_url()
    tit = title and safe_unicode(title) or safe_unicode(obj.Title())
    return u'<a href="%s">%s</a>' % (href, tit)


class ProjectSoapClientView(BrowserView):
    """ Adapts an action or task to prepare data to exchange within imio.pm.wsclient """

    def motivation(self):
        return ("<p></p>")

    def common_detailed_description(self):
        out = []
        out.append(u"<p>OS: %s</p>" % object_link(self.os))
        out.append(u"<p>OO: %s</p>" % object_link(self.oo))
        out.append(u"<p>Action: %s</p>" % object_link(self.action))
        hasattr(self, 'sa') and out.append(u"<p>Sous-action: %s</p>" % object_link(self.sa))
        return out

    def description(self):
        return safe_unicode(self.action.Description())


class ProjectActionSoapClientView(ProjectSoapClientView):

    def __init__(self, context, request):
        super(ProjectActionSoapClientView, self).__init__(context, request)
        self.action = self.context
        self.oo = self.action.aq_parent
        self.os = self.oo.aq_parent

    def detailed_description(self):
        return u''.join(self.common_detailed_description())


class ProjectSubActionSoapClientView(ProjectSoapClientView):

    def __init__(self, context, request):
        super(ProjectSubActionSoapClientView, self).__init__(context, request)
        self.sa = self.context
        self.action = self.sa.aq_parent
        self.oo = self.action.aq_parent
        self.os = self.oo.aq_parent

    def detailed_description(self):
        return u''.join(self.common_detailed_description())


class ProjectTaskSoapClientView(ProjectSoapClientView):

    def __init__(self, context, request):
        super(ProjectTaskSoapClientView, self).__init__(context, request)
        self.adapted = ITaskMethods(self.context)
        if self.adapted.get_highest_task_parent(task=False).portal_type == 'pstsubaction':
            self.sa = self.adapted.get_highest_task_parent(task=False)
            self.action = self.sa.aq_parent
        else:
            self.action = self.adapted.get_highest_task_parent(task=False)
        self.oo = self.action.aq_parent
        self.os = self.oo.aq_parent

    def detailed_description(self):
        out = self.common_detailed_description()
        out.append(u"<p>Tâche: %s</p>" % object_link(self.context, title=self.adapted.get_full_tree_title()))
        return u''.join(out)

    def description(self):
        if self.context.task_description:
            return safe_unicode(self.context.task_description.output)
        return None
