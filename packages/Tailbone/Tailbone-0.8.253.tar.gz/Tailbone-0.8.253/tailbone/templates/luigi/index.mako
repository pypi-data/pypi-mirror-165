## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">View / Launch Tasks</%def>

<%def name="page_content()">
  <br />
  <div class="form">

    <div class="buttons">

      <b-button tag="a"
                % if luigi_url:
                href="${luigi_url}"
                % else:
                href="#" disabled
                title="Luigi URL is not configured"
                % endif
                icon-pack="fas"
                icon-left="external-link-alt"
                target="_blank">
        Luigi Task Visualiser
      </b-button>

      <b-button tag="a"
                % if luigi_history_url:
                href="${luigi_history_url}"
                % else:
                href="#" disabled
                title="Luigi URL is not configured"
                % endif
                icon-pack="fas"
                icon-left="external-link-alt"
                target="_blank">
        Luigi Task History
      </b-button>

      % if master.has_perm('restart_scheduler'):
          ${h.form(url('{}.restart_scheduler'.format(route_prefix)), **{'@submit': 'submitRestartSchedulerForm'})}
          ${h.csrf_token(request)}
          <b-button type="is-primary"
                    native-type="submit"
                    icon-pack="fas"
                    icon-left="redo"
                    :disabled="restartSchedulerFormSubmitting">
            {{ restartSchedulerFormSubmitting ? "Working, please wait..." : "Restart Luigi Scheduler" }}
          </b-button>
          ${h.end_form()}
      % endif
    </div>

    % if  master.has_perm('launch_overnight'):

        <h3 class="block is-size-3">Overnight Tasks</h3>

        <b-table :data="overnightTasks" hoverable>
          <template slot-scope="props">
            <b-table-column field="description"
                            label="Description">
              {{ props.row.description }}
            </b-table-column>
            <b-table-column field="script"
                            label="Script">
              {{ props.row.script }}
            </b-table-column>
            <b-table-column field="last_date"
                            label="Last Date"
                            :class="overnightTextClass(props.row)">
              {{ props.row.last_date || "never!" }}
            </b-table-column>
            <b-table-column label="Actions">
              <b-button type="is-primary"
                        icon-pack="fas"
                        icon-left="arrow-circle-right"
                        :disabled="overnightTaskLaunching == props.row.key"
                        @click="overnightTaskLaunch(props.row)">
                {{ overnightTaskLaunching == props.row.key ? "Working, please wait..." : "Launch" }}
              </b-button>
            </b-table-column>
          </template>
          <template #empty>
            <p class="block">No tasks defined.</p>
          </template>
        </b-table>

    % endif

    % if master.has_perm('launch_backfill'):

        <h3 class="block is-size-3">Backfill Tasks</h3>

        <b-table :data="backfillTasks" hoverable>
          <template slot-scope="props">
            <b-table-column field="description"
                            label="Description">
              {{ props.row.description }}
            </b-table-column>
            <b-table-column field="script"
                            label="Script">
              {{ props.row.script }}
            </b-table-column>
            <b-table-column field="forward"
                            label="Orientation">
              {{ props.row.forward ? "Forward" : "Backward" }}
            </b-table-column>
            <b-table-column field="last_date"
                            label="Last Date"
                            :class="backfillTextClass(props.row)">
              {{ props.row.last_date }}
            </b-table-column>
            <b-table-column field="target_date"
                            label="Target Date">
              {{ props.row.target_date }}
            </b-table-column>
            <b-table-column label="Actions">
              <b-button type="is-primary"
                        icon-pack="fas"
                        icon-left="arrow-circle-right"
                        @click="backfillTaskLaunch(props.row)">
                Launch
              </b-button>
            </b-table-column>
          </template>
          <template #empty>
            <p class="block">No tasks defined.</p>
          </template>
        </b-table>

        <b-modal has-modal-card
                 :active.sync="backfillTaskShowLaunchDialog">
          <div class="modal-card">

            <header class="modal-card-head">
              <p class="modal-card-title">Launch Backfill Task</p>
            </header>

            <section class="modal-card-body"
                     v-if="backfillTask">

              <p class="block has-text-weight-bold">
                {{ backfillTask.description }}
                (goes {{ backfillTask.forward ? "FORWARD" : "BACKWARD" }})
              </p>

              <b-field grouped>
                <b-field label="Last Date">
                  {{ backfillTask.last_date || "n/a" }}
                </b-field>
                <b-field label="Target Date">
                  {{ backfillTask.target_date || "n/a" }}
                </b-field>
              </b-field>

              <b-field grouped>

                <b-field label="Start Date"
                         :type="backfillTaskStartDate ? null : 'is-danger'">
                  <tailbone-datepicker v-model="backfillTaskStartDate">
                  </tailbone-datepicker>
                </b-field>

                <b-field label="End Date"
                         :type="backfillTaskEndDate ? null : 'is-danger'">
                  <tailbone-datepicker v-model="backfillTaskEndDate">
                  </tailbone-datepicker>
                </b-field>

              </b-field>

            </section>

            <footer class="modal-card-foot">
              <b-button @click="backfillTaskShowLaunchDialog = false">
                Cancel
              </b-button>
              <b-button type="is-primary"
                        icon-pack="fas"
                        icon-left="arrow-circle-right"
                        @click="backfillTaskLaunchSubmit()"
                        :disabled="backfillTaskLaunching || !backfillTaskStartDate || !backfillTaskEndDate">
                {{ backfillTaskLaunching ? "Working, please wait..." : "Launch" }}
              </b-button>
            </footer>
          </div>
        </b-modal>

    % endif

  </div>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if master.has_perm('restart_scheduler'):

        ThisPageData.restartSchedulerFormSubmitting = false

        ThisPage.methods.submitRestartSchedulerForm = function() {
            this.restartSchedulerFormSubmitting = true
        }

    % endif

    % if master.has_perm('launch_overnight'):

        ThisPageData.overnightTasks = ${json.dumps(overnight_tasks)|n}
        ThisPageData.overnightTaskLaunching = false

        ThisPage.methods.overnightTextClass = function(task) {
            let yesterday = '${rattail_app.today() - datetime.timedelta(days=1)}'
            if (task.last_date) {
                if (task.last_date == yesterday) {
                    return 'has-text-success'
                } else {
                    return 'has-text-warning'
                }
            } else {
                return 'has-text-warning'
            }
        }

        ThisPage.methods.overnightTaskLaunch = function(task) {
            this.overnightTaskLaunching = task.key

            let url = '${url('{}.launch_overnight'.format(route_prefix))}'
            let params = {key: task.key}

            this.submitForm(url, params, response => {
                this.$buefy.toast.open({
                    message: "Task has been scheduled for immediate launch!",
                    type: 'is-success',
                    duration: 5000, // 5 seconds
                })
                this.overnightTaskLaunching = false
            })
        }

    % endif

    % if master.has_perm('launch_backfill'):

        ThisPageData.backfillTasks = ${json.dumps(backfill_tasks)|n}
        ThisPageData.backfillTask = null
        ThisPageData.backfillTaskStartDate = null
        ThisPageData.backfillTaskEndDate = null
        ThisPageData.backfillTaskShowLaunchDialog = false
        ThisPageData.backfillTaskLaunching = false

        ThisPage.methods.backfillTextClass = function(task) {
            if (task.target_date) {
                if (task.last_date) {
                    if (task.forward) {
                        if (task.last_date >= task.target_date) {
                            return 'has-text-success'
                        } else {
                            return 'has-text-warning'
                        }
                    } else {
                        if (task.last_date <= task.target_date) {
                            return 'has-text-success'
                        } else {
                            return 'has-text-warning'
                        }
                    }
                }
            }
        }

        ThisPage.methods.backfillTaskLaunch = function(task) {
            this.backfillTask = task
            this.backfillTaskStartDate = null
            this.backfillTaskEndDate = null
            this.backfillTaskShowLaunchDialog = true
        }

        ThisPage.methods.backfillTaskLaunchSubmit = function() {
            this.backfillTaskLaunching = true

            let url = '${url('{}.launch_backfill'.format(route_prefix))}'
            let params = {
                key: this.backfillTask.key,
                start_date: this.backfillTaskStartDate,
                end_date: this.backfillTaskEndDate,
            }

            this.submitForm(url, params, response => {
                this.$buefy.toast.open({
                    message: "Task has been scheduled for immediate launch!",
                    type: 'is-success',
                    duration: 5000, // 5 seconds
                })
                this.backfillTaskLaunching = false
                this.backfillTaskShowLaunchDialog = false
            })
        }

    % endif

  </script>
</%def>


${parent.body()}
