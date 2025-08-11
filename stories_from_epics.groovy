// This script will create one story for each value in a multi-select list and set summary, description, epic link, reporter

import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.issue.IssueFactory
import com.atlassian.jira.issue.IssueManager
import com.atlassian.jira.issue.MutableIssue
import com.atlassian.jira.issue.fields.CustomField
import com.atlassian.jira.user.ApplicationUser
import com.atlassian.jira.issue.util.DefaultIssueChangeHolder
import com.atlassian.jira.issue.ModifiedValue
import com.atlassian.jira.issue.customfields.option.Option

def issue = event.issue
def issueType = issue.issueType.name

if (issueType != "Epic") {
    return
}

def issueManager = ComponentAccessor.getIssueManager()
def issueFactory = ComponentAccessor.getIssueFactory()
def cfManager = ComponentAccessor.getCustomFieldManager()
def user = ComponentAccessor.getJiraAuthenticationContext().getLoggedInUser()
def constantsManager = ComponentAccessor.getConstantsManager()

CustomField theCustomField = cfManager.getCustomFieldObjectByName("The Custom Field Name")
def values = issue.getCustomFieldValue(theCustomField) as List<Option>

CustomField epicLinkField = cfManager.getCustomFieldObjectByName("Epic Link")
def storyIssueType = constantsManager.getAllIssueTypeObjects().find { it.name == "Story"}

values.each { Option value ->
    MutableIssue newIssue = issueFactory.getIssue()
    newIssue.setProjectObject(issue.getProjectObject())
    newIssue.setIssueTypeId(storyIssueType.id)
    newIssue.setSummary("Audit for ${value.getValue()}")
    newIssue.setDescription("Audit user access for ${value.getValue()}")
    newIssue.setReporter(user)
    
    issueManager.createIssueObject(user, newIssue)
    
    epicLinkField.updateValue(null, newIssue, new ModifiedValue(null, issue), new DefaultIssueChangeHolder())
}