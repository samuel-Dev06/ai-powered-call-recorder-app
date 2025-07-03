import { NavItem } from './nav-item/nav-item';

export const navItems: NavItem[] = [
  {
    navCap: 'Home',
  },
  {
    displayName: 'Dashboard',
    iconName: 'solar:home-angle-broken',
    route: '/home/dashboard',
  },
  {
    navCap: 'Call Management',
    divider: true
  },
  {
    displayName: 'Live Record',
    iconName: 'solar:call-chat-broken',
    route: '/home/call/live-record',
  },
  {
    displayName: 'Upload Record',
    iconName: 'solar:upload-outline',
    route: '/home/call/upload-record',
  },
  {
    navCap: 'Reports',
    divider: true
  },
  {
    displayName: 'Recordings',
    iconName: 'solar:microphone-2-broken',
    route: '/home/call/report',
  },

  {
    navCap: 'Subscription Management',
    divider: true
  },
  {
    displayName: 'Pricing',
    iconName: 'solar:dollar-minimalistic-broken',
    route: '/subscription/pricing',
  },{
    displayName: 'Documentation',
    iconName: 'solar:document-add-broken',
    route: '/subscription/documentation',
  },


  
];
