export class AccountSettingsController {
  
  userAccount;

  constructor(AppApi, $stateParams, $mdDialog, $mdToast, $state) {
    this.AppApi = AppApi;
    this.$stateParams = $stateParams;
    this.$mdDialog = $mdDialog;
    this.$mdToast = $mdToast;
    this.$state = $state;
    this.userAccount = {};
  }

  $onInit() {
    if (this.$stateParams.accountId) {
      this.AppApi.getUserAccount(this.$stateParams.accountId)
        .then((successResponse) => {
          this.userAccount = successResponse.data;
        }, (errorResponse) => {
          this.userAccount = null;
        });
    } else {
      this.userAccount = null;
    }
  }

  deleteAccount() {
    this.AppApi.deleteUserAccount(this.$stateParams.accountId)
      .then((successResponse) => {
        this.$state.go("accountList");
        this.$mdToast.show(this.$mdToast.simple().textContent('Your integration has been successfully removed'));
      }, (errorResponse) => {
        this.$mdToast.show(this.$mdToast.simple().textContent('Unable to remove your account at the moment'));
      });
  }

  onDeleteAccount() {
    var confirm = this.$mdDialog.prompt()
          .title("Would you like to remove this Statuspage integration with Yellowant?")
          .textContent(`Please type in your Statuspage handle to confirm: ${this.userAccount.handle}`)
          .placeholder("statuspage-handle")
          .ariaLabel("statuspage Handle")
          .clickOutsideToClose(true)
          .ok('Delete Integration')
          .cancel('Cancel');

    this.$mdDialog.show(confirm).then((result) =>
    {
      if (result == this.userAccount.handle) {
        this.deleteAccount(this.$stateParams.accountId);
      }
      else
        this.onDeleteAccount();
    }, function() { });
  }

  onDeleteWebhook(webhook) {
    var confirm = this.$mdDialog.confirm()
          .title(`Would you like to remove your webhook ${webhook.id} for "${webhook.repo_full_name}"?`)
          .clickOutsideToClose(true)
          .ok('Delete Webhook')
          .cancel('Cancel');

    this.$mdDialog.show(confirm).then(() =>
    {
      this.deleteWebhook(webhook);
    }, function() { });
  }

  deleteWebhook(webhook) {
    this.AppApi.deleteUserWebhook(this.$stateParams.accountId, webhook.id)
      .then((successResponse) => {
        this.$mdToast.show(this.$mdToast.simple().textContent('Deleted webhook successfully!'));
        webhook.is_deleted = true;
      }, (errorResponse) => {
        this.$mdToast.show(this.$mdToast.simple().textContent('Unable to delete the webhook at the moment'));
      });
  }
}