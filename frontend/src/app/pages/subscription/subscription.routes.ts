import {Routes} from "@angular/router";
import {ApiDocumentationComponent} from "./api-documentation/api-documentation.component";
import {ApiPricingComponent} from "./api-pricing/api-pricing.component";

export const SubscriptionRoutes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'pricing',
                component: ApiPricingComponent,
            },
            {
                path: 'documentation',
                component: ApiDocumentationComponent,
            },
        ],
    },
];