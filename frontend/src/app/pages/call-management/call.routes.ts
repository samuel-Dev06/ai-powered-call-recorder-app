import {Routes} from "@angular/router";
import {AppSideLoginComponent} from "../authentication/side-login/side-login.component";
import {AppSideRegisterComponent} from "../authentication/side-register/side-register.component";
import {LiveCallComponent} from "./live-call/live-call.component";
import {UploadCallComponent} from "./upload-call/upload-call.component";
import {CallReportsComponent} from "./call-reports/call-reports.component";

export const CallRoutes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'live-record',
                component: LiveCallComponent,
            },
            {
                path: 'upload-record',
                component: UploadCallComponent,
            },
            {
                path: 'report',
                component: CallReportsComponent,
            }
        ],
    },
];