edx = edx || {};

((Backbone, $, _) => {
  'use strict';

  edx.instructor_dashboard = edx.instructor_dashboard || {};
  edx.instructor_dashboard.proctoring = edx.instructor_dashboard.proctoring || {};
  edx.instructor_dashboard.proctoring.ProctoredExamDashboardView = Backbone.View.extend({
    initialize() {
      const self = this;
      this.setElement($('.student-review-dashboard-container'));
      this.template_url = '/static/proctoring/templates/dashboard.underscore';
      this.iframeHTML = null;
      this.doRender = true;
      this.context = {
        dashboardURL: `/api/edx_proctoring/v1/instructor/${this.$el.data('course-id')}`,
      };

      $('#proctoring-accordion').on('accordionactivate', (event, ui) => {
        self.render(ui);
      });
      /* Load the static template for rendering. */
      this.loadTemplateData();
    },
    loadTemplateData() {
      const self = this;
      $.ajax({ url: self.template_url, dataType: 'html' })
        .done((templateHtml) => {
          self.iframeHTML = _.template(templateHtml)(self.context);
        });
    },
    render(ui) {
      if (ui.newPanel.eq(this.$el) && this.doRender && this.iframeHTML) {
        this.$el.html(this.iframeHTML);
        this.doRender = false;
      }
    },
  });
  const proctoredExamDashboardView = edx.instructor_dashboard.proctoring.ProctoredExamDashboardView;
  this.edx.instructor_dashboard.proctoring.ProctoredExamDashboardView = proctoredExamDashboardView;
}).call(this, Backbone, $, _);
