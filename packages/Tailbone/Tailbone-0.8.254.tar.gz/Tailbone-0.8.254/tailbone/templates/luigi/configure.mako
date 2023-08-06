## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">
  ${h.hidden('overnight_tasks', **{':value': 'JSON.stringify(overnightTasks)'})}
  ${h.hidden('backfill_tasks', **{':value': 'JSON.stringify(backfillTasks)'})}

  <div class="level">
    <div class="level-left">
      <div class="level-item">
        <h3 class="is-size-3">Overnight Tasks</h3>
      </div>
      <div class="level-item">
        <b-button type="is-primary"
                  icon-pack="fas"
                  icon-left="plus"
                  @click="overnightTaskCreate()">
          New Task
        </b-button>
      </div>
    </div>
  </div>
  <div class="block" style="padding-left: 2rem; display: flex;">

    <b-table :data="overnightTasks">
      <template slot-scope="props">
        <!-- <b-table-column field="key" -->
        <!--                 label="Key" -->
        <!--                 sortable> -->
        <!--   {{ props.row.key }} -->
        <!-- </b-table-column> -->
        <b-table-column field="description"
                        label="Description">
          {{ props.row.description }}
        </b-table-column>
        <b-table-column field="script"
                        label="Script">
          {{ props.row.script }}
        </b-table-column>
        <b-table-column label="Actions">
          <a href="#"
             @click.prevent="overnightTaskEdit(props.row)">
            <i class="fas fa-edit"></i>
            Edit
          </a>
          &nbsp;
          <a href="#"
             class="has-text-danger"
             @click.prevent="overnightTaskDelete(props.row)">
            <i class="fas fa-trash"></i>
            Delete
          </a>
        </b-table-column>
      </template>
    </b-table>

    <b-modal has-modal-card
             :active.sync="overnightTaskShowDialog">
      <div class="modal-card">

        <header class="modal-card-head">
          <p class="modal-card-title">Overnight Task</p>
        </header>

        <section class="modal-card-body">
          <!-- <b-field label="Key"> -->
          <!--   <b-input v-model.trim="overnightTaskKey" -->
          <!--            ref="overnightTaskKey"> -->
          <!--   </b-input> -->
          <!-- </b-field> -->
          <b-field label="Description"
                   :type="overnightTaskDescription ? null : 'is-danger'">
            <b-input v-model.trim="overnightTaskDescription"
                     ref="overnightTaskDescription">
            </b-input>
          </b-field>
          <b-field label="Script"
                   :type="overnightTaskScript ? null : 'is-danger'">
            <b-input v-model.trim="overnightTaskScript">
            </b-input>
          </b-field>
          <b-field label="Notes">
            <b-input v-model.trim="overnightTaskNotes"
                     type="textarea">
            </b-input>
          </b-field>
        </section>

        <footer class="modal-card-foot">
          <b-button type="is-primary"
                    icon-pack="fas"
                    icon-left="save"
                    @click="overnightTaskSave()"
                    :disabled="!overnightTaskDescription || !overnightTaskScript">
            Save
          </b-button>
          <b-button @click="overnightTaskShowDialog = false">
            Cancel
          </b-button>
        </footer>
      </div>
    </b-modal>

  </div>

  <div class="level">
    <div class="level-left">
      <div class="level-item">
        <h3 class="is-size-3">Backfill Tasks</h3>
      </div>
      <div class="level-item">
        <b-button type="is-primary"
                  icon-pack="fas"
                  icon-left="plus"
                  @click="backfillTaskCreate()">
          New Task
        </b-button>
      </div>
    </div>
  </div>
  <div class="block" style="padding-left: 2rem; display: flex;">

    <b-table :data="backfillTasks">
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
        <b-table-column field="target_date"
                        label="Target Date">
          {{ props.row.target_date }}
        </b-table-column>
        <b-table-column label="Actions">
          <a href="#"
             @click.prevent="backfillTaskEdit(props.row)">
            <i class="fas fa-edit"></i>
            Edit
          </a>
          &nbsp;
          <a href="#"
             class="has-text-danger"
             @click.prevent="backfillTaskDelete(props.row)">
            <i class="fas fa-trash"></i>
            Delete
          </a>
        </b-table-column>
      </template>
    </b-table>

    <b-modal has-modal-card
             :active.sync="backfillTaskShowDialog">
      <div class="modal-card">

        <header class="modal-card-head">
          <p class="modal-card-title">Backfill Task</p>
        </header>

        <section class="modal-card-body">
          <b-field label="Description"
                   :type="backfillTaskDescription ? null : 'is-danger'">
            <b-input v-model.trim="backfillTaskDescription"
                     ref="backfillTaskDescription">
            </b-input>
          </b-field>
          <b-field label="Script"
                   :type="backfillTaskScript ? null : 'is-danger'">
            <b-input v-model.trim="backfillTaskScript">
            </b-input>
          </b-field>
          <b-field grouped>
            <b-field label="Orientation">
              <b-select v-model="backfillTaskForward">
                <option :value="false">Backward</option>
                <option :value="true">Forward</option>
              </b-select>
            </b-field>
            <b-field label="Target Date">
              <tailbone-datepicker v-model="backfillTaskTargetDate">
              </tailbone-datepicker>
            </b-field>
          </b-field>
          <b-field label="Notes">
            <b-input v-model.trim="backfillTaskNotes"
                     type="textarea">
            </b-input>
          </b-field>
        </section>

        <footer class="modal-card-foot">
          <b-button type="is-primary"
                    icon-pack="fas"
                    icon-left="save"
                    @click="backfillTaskSave()"
                    :disabled="!backfillTaskDescription || !backfillTaskScript">
            Save
          </b-button>
          <b-button @click="backfillTaskShowDialog = false">
            Cancel
          </b-button>
        </footer>
      </div>
    </b-modal>

  </div>

  <h3 class="is-size-3">Luigi Proper</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field label="Luigi URL"
             message="This should be the URL to Luigi Task Visualiser web user interface."
             expanded>
      <b-input name="rattail.luigi.url"
               v-model="simpleSettings['rattail.luigi.url']"
               @input="settingsNeedSaved = true">
      </b-input>
    </b-field>

    <b-field label="Supervisor Process Name"
             message="This should be the complete name, including group - e.g. luigi:luigid"
             expanded>
      <b-input name="rattail.luigi.scheduler.supervisor_process_name"
               v-model="simpleSettings['rattail.luigi.scheduler.supervisor_process_name']"
               @input="settingsNeedSaved = true">
      </b-input>
    </b-field>

    <b-field label="Restart Command"
             message="This will run as '${system_user}' system user - please configure sudoers as needed.  Typical command is like:  sudo supervisorctl restart luigi:luigid"
             expanded>
      <b-input name="rattail.luigi.scheduler.restart_command"
               v-model="simpleSettings['rattail.luigi.scheduler.restart_command']"
               @input="settingsNeedSaved = true">
      </b-input>
    </b-field>

  </div>

</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.overnightTasks = ${json.dumps(overnight_tasks)|n}
    ThisPageData.overnightTaskShowDialog = false
    ThisPageData.overnightTask = null
    ThisPageData.overnightTaskCounter = 0
    ThisPageData.overnightTaskKey = null
    ThisPageData.overnightTaskDescription = null
    ThisPageData.overnightTaskScript = null
    ThisPageData.overnightTaskNotes = null

    ThisPage.methods.overnightTaskCreate = function() {
        this.overnightTask = {key: null}
        this.overnightTaskKey = null
        this.overnightTaskDescription = null
        this.overnightTaskScript = null
        this.overnightTaskNotes = null
        this.overnightTaskShowDialog = true
        this.$nextTick(() => {
            this.$refs.overnightTaskDescription.focus()
        })
    }

    ThisPage.methods.overnightTaskEdit = function(task) {
        this.overnightTask = task
        this.overnightTaskKey = task.key
        this.overnightTaskDescription = task.description
        this.overnightTaskScript = task.script
        this.overnightTaskNotes = task.notes
        this.overnightTaskShowDialog = true
    }

    ThisPage.methods.overnightTaskSave = function() {
        this.overnightTask.description = this.overnightTaskDescription
        this.overnightTask.script = this.overnightTaskScript
        this.overnightTask.notes = this.overnightTaskNotes

        if (!this.overnightTask.key) {
            this.overnightTask.key = `_new_${'$'}{++this.overnightTaskCounter}`
            this.overnightTasks.push(this.overnightTask)
        }

        this.overnightTaskShowDialog = false
        this.settingsNeedSaved = true
    }

    ThisPage.methods.overnightTaskDelete = function(task) {
        if (confirm("Really delete this task?")) {
            let i = this.overnightTasks.indexOf(task)
            this.overnightTasks.splice(i, 1)
            this.settingsNeedSaved = true
        }
    }

    ThisPageData.backfillTasks = ${json.dumps(backfill_tasks)|n}
    ThisPageData.backfillTaskShowDialog = false
    ThisPageData.backfillTask = null
    ThisPageData.backfillTaskCounter = 0
    ThisPageData.backfillTaskKey = null
    ThisPageData.backfillTaskDescription = null
    ThisPageData.backfillTaskScript = null
    ThisPageData.backfillTaskForward = false
    ThisPageData.backfillTaskTargetDate = null
    ThisPageData.backfillTaskNotes = null

    ThisPage.methods.backfillTaskCreate = function() {
        this.backfillTask = {key: null}
        this.backfillTaskDescription = null
        this.backfillTaskScript = null
        this.backfillTaskForward = false
        this.backfillTaskTargetDate = null
        this.backfillTaskNotes = null
        this.backfillTaskShowDialog = true
        this.$nextTick(() => {
            this.$refs.backfillTaskDescription.focus()
        })
    }

    ThisPage.methods.backfillTaskEdit = function(task) {
        this.backfillTask = task
        this.backfillTaskDescription = task.description
        this.backfillTaskScript = task.script
        this.backfillTaskForward = task.forward
        this.backfillTaskTargetDate = task.target_date
        this.backfillTaskNotes = task.notes
        this.backfillTaskShowDialog = true
    }

    ThisPage.methods.backfillTaskDelete = function(task) {
        if (confirm("Really delete this task?")) {
            let i = this.backfillTasks.indexOf(task)
            this.backfillTasks.splice(i, 1)
            this.settingsNeedSaved = true
        }
    }

    ThisPage.methods.backfillTaskSave = function() {
        this.backfillTask.description = this.backfillTaskDescription
        this.backfillTask.script = this.backfillTaskScript
        this.backfillTask.forward = this.backfillTaskForward
        this.backfillTask.target_date = this.backfillTaskTargetDate
        this.backfillTask.notes = this.backfillTaskNotes

        if (!this.backfillTask.key) {
            this.backfillTask.key = `_new_${'$'}{++this.backfillTaskCounter}`
            this.backfillTasks.push(this.backfillTask)
        }

        this.backfillTaskShowDialog = false
        this.settingsNeedSaved = true
    }

  </script>
</%def>


${parent.body()}
